import os
import re
import nltk
import numpy as np
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer
from codebleu import calc_codebleu
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import torch
from transformers import AutoTokenizer, AutoModel
from openai import OpenAI, APIError, APIConnectionError

# ------------------------------------------------------------------------------------------------
# Preprocessing for Code Similarity
# ------------------------------------------------------------------------------------------------

def preprocess_java_code(code: str) -> str:
    lines = code.splitlines()
    lines = [line for line in lines if not line.strip().startswith("import")]
    lines = [line for line in lines if line.strip()]
    return "\n".join(lines).strip()

def clean_code_for_embedding(code: str) -> str:
    code = re.sub(r"//.*", "", code)
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    return "\n".join([line for line in code.split("\n") if line.strip()])

# ------------------------------------------------------------------------------------------------
# Metric Computation
# ------------------------------------------------------------------------------------------------

def calculate_codebleu(reference: str, prediction: str) -> dict:
    return calc_codebleu(
        references=[reference],
        predictions=[prediction],
        lang="java",
        weights=(0.25, 0.25, 0.25, 0.25),
        tokenizer=None
    )

def calculate_rouge_l(reference: str, prediction: str) -> float:
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=False)
    return scorer.score(reference, prediction)['rougeL'].fmeasure

def calculate_meteor(reference: str, prediction: str) -> float:
    return meteor_score([reference.split()], prediction.split())

def ensure_nltk():
    nltk.data.path.append(".")
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", download_dir=".")

# ------------------------------------------------------------------------------------------------
# Composite Score (CTSES)
# ------------------------------------------------------------------------------------------------

def compute_ctses(codebleu: float, meteor: float, rouge: float) -> dict:
    return {
        "CTSES_Avg": round((codebleu + meteor + rouge) / 3, 4),
        "CTSES_1": round(0.5 * codebleu + 0.3 * meteor + 0.2 * rouge, 4),
        "CTSES_2": round(0.4 * codebleu + 0.3 * meteor + 0.3 * rouge, 4)
    }

# ------------------------------------------------------------------------------------------------
# Embedding-based Similarities
# ------------------------------------------------------------------------------------------------

def get_transformer_embedding(text: str, model_name: str) -> np.ndarray:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).cpu().numpy()

def get_openai_embedding(text: str) -> np.ndarray:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OPENAI_API_KEY in .env file")
    client = OpenAI(api_key=api_key)
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return np.array(response.data[0].embedding)
    except (APIError, APIConnectionError) as e:
        print(f"[OpenAI ERROR] {e}")
        return None

def compute_cosine_similarity(emb1: np.ndarray, emb2: np.ndarray) -> float:
    return float(cosine_similarity(emb1.reshape(1, -1), emb2.reshape(1, -1))[0][0])

# ------------------------------------------------------------------------------------------------
# Main Evaluation
# ------------------------------------------------------------------------------------------------

def evaluate(reference: str, prediction: str):
    ensure_nltk()

    print("=" * 100)
    print("EVALUATING LEXICAL AND STRUCTURAL SIMILARITY (CodeBLEU, METEOR, ROUGE-L, CTSES)")
    print("=" * 100)

    codebleu_ref = preprocess_java_code(reference)
    codebleu_pred = preprocess_java_code(prediction)
    codebleu_result = calculate_codebleu(codebleu_ref, codebleu_pred)
    meteor = calculate_meteor(reference, prediction)
    rouge_l = calculate_rouge_l(reference, prediction)

    print(f"[CodeBLEU] Score                 : {codebleu_result['codebleu']:.4f}")
    print(f"  - N-Gram Match                : {codebleu_result['ngram_match_score']:.4f}")
    print(f"  - Weighted N-Gram            : {codebleu_result['weighted_ngram_match_score']:.4f}")
    print(f"  - Syntax Match               : {codebleu_result['syntax_match_score']:.4f}")
    print(f"  - Dataflow Match             : {codebleu_result['dataflow_match_score']:.4f}")
    print(f"[METEOR]                        : {meteor:.4f}")
    print(f"[ROUGE-L]                       : {rouge_l:.4f}")

    ctses = compute_ctses(codebleu_result['codebleu'], meteor, rouge_l)
    print(f"[CTSES - Average]               : {ctses['CTSES_Avg']:.4f}")
    print(f"[CTSES - (0.5, 0.3, 0.2)]       : {ctses['CTSES_1']:.4f}")
    print(f"[CTSES - (0.4, 0.3, 0.3)]       : {ctses['CTSES_2']:.4f}")

    print("\n\n" + "=" * 100)
    print("EVALUATING SEMANTIC SIMILARITY (CodeBERT, GraphCodeBERT, OpenAI)")
    print("=" * 100)

    cleaned_ref = clean_code_for_embedding(reference)
    cleaned_pred = clean_code_for_embedding(prediction)

    print("\n[CodeBERT] Computing embeddings...")
    emb1 = get_transformer_embedding(cleaned_ref, "microsoft/codebert-base")
    emb2 = get_transformer_embedding(cleaned_pred, "microsoft/codebert-base")
    print(f"Cosine Similarity (CodeBERT)     : {compute_cosine_similarity(emb1, emb2):.4f}")

    print("\n[GraphCodeBERT] Computing embeddings...")
    emb1 = get_transformer_embedding(cleaned_ref, "microsoft/graphcodebert-base")
    emb2 = get_transformer_embedding(cleaned_pred, "microsoft/graphcodebert-base")
    print(f"Cosine Similarity (GraphCodeBERT): {compute_cosine_similarity(emb1, emb2):.4f}")

    print("\n[OpenAI] Computing embeddings...")
    emb1 = get_openai_embedding(cleaned_ref)
    emb2 = get_openai_embedding(cleaned_pred)
    if emb1 is not None and emb2 is not None:
        print(f"Cosine Similarity (OpenAI)       : {compute_cosine_similarity(emb1, emb2):.4f}")
    else:
        print("OpenAI embedding failed or skipped.")

    print("=" * 100)


# ------------------------------------------------------------------------------------------------
# Example Usage
# ------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    from examples.macaw_tests import reference_test, prediction_test
    evaluate(reference_test, prediction_test)
