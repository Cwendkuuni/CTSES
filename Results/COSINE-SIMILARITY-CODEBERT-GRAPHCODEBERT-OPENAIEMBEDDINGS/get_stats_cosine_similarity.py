import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

# === Configuration ===
INPUT_DIR = Path(".")
OUTPUT_DIR = Path("cosine_similarity_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

FILENAME_PATTERN = re.compile(
    r"(Defects4J|SF110)-Scenario-1-similarity-(CODEBERT|GRAPHCODEBERT|OPENAI)-(GPT|MISTRAL)\.json",
    re.IGNORECASE
)

# === Lecture et extraction ===
def load_similarity_data():
    records = []
    for file in INPUT_DIR.glob("*.json"):
        match = FILENAME_PATTERN.match(file.name)
        if not match:
            continue

        dataset, embedding_raw, model_raw = match.groups()
        model = "GPT 4-o" if model_raw.upper() == "GPT" else "Mistral large-2407"
        embedding = (
            "GraphCodeBERT" if embedding_raw.upper() == "GRAPHCODEBERT" else
            "CodeBERT" if embedding_raw.upper() == "CODEBERT" else
            "OpenAI"
        )

        with open(file, "r") as f:
            data = json.load(f)
            for entry in data:
                similarity = entry.get("cosine_similarity")
                if similarity is not None:
                    records.append({
                        "Dataset": dataset,
                        "Model": model,
                        "Embedding": embedding,
                        "Cosine Similarity": similarity
                    })
    return pd.DataFrame(records)

# === Statistiques ===
def compute_stats(df, group_cols, value_col):
    return df.groupby(group_cols)[value_col].agg([
        ("Min", "min"),
        ("Q1", lambda x: np.percentile(x.dropna(), 25)),
        ("Median", "median"),
        ("Q3", lambda x: np.percentile(x.dropna(), 75)),
        ("Max", "max"),
        ("Mean", "mean")
    ]).reset_index()

# === Export CSV ===
def export_csv(df, filename):
    path = OUTPUT_DIR / filename
    df.to_csv(path, index=False)
    print(f"- {filename}")

# === Main execution ===
def main():
    df = load_similarity_data()
    if df.empty:
        print("Aucun fichier JSON valide trouvé.")
        return

    stats_detailed = compute_stats(df, ["Dataset", "Model", "Embedding"], "Cosine Similarity")
    stats_global = compute_stats(df, ["Embedding"], "Cosine Similarity")

    export_csv(stats_detailed, "cosine_similarity_stats_detailed.csv")
    export_csv(stats_global, "cosine_similarity_stats_global.csv")

if __name__ == "__main__":
    main()
