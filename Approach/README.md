# CTSES: A Composite Metric for Evaluating Test Refactoring

This folder implements **CTSES** (Composite Test Similarity Evaluation Score), a semantics-driven metric for assessing the quality of unit test refactorings produced by Large Language Models (LLMs). CTSES addresses the limitations of traditional similarity metrics such as CodeBLEU, by integrating **lexical**, **structural**, and **semantic** signals into a unified, interpretable score.

This implementation reproduces the **motivating example** presented in our paper:

> **Beyond CodeBLEU: Rethinking Test Refactoring Evaluation with Semantics-Driven and Behavior-Preserving Metrics**  

---

## Objective

Test refactoring aims to improve readability, naming, and structure while **preserving behavior**. However, most similarity metrics fail to capture these goals:

- CodeBLEU is overly sensitive to lexical changes (e.g., renaming, reordering).
- Cosine similarity captures semantics but ignores readability and structure.
- METEOR and ROUGE-L only partially reflect structure or clarity.

**CTSES** integrates all these perspectives into a configurable score that aligns with **developer intuition**.

---

## Folder Structure

```
Approach/
├── evaluate_test_similarity.py       # Main script for evaluation
├── examples/                         # Contains input reference and prediction test pairs
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

---

## 🧪 Evaluation Metrics

We compute both **lexical/structural** metrics and **semantic** similarities:

| Metric         | Type        | Description                                                   |
|----------------|-------------|---------------------------------------------------------------|
| **CodeBLEU**   | Lexical     | Combines n-gram, syntax, and dataflow similarity              |
| **METEOR**     | Lexical     | Matches lexical tokens, synonyms, stems                       |
| **ROUGE-L**    | Structural  | Measures Longest Common Subsequence                           |
| **CTSES**      | Composite   | Weighted score of CodeBLEU, METEOR, and ROUGE-L               |
| **Cosine Sim.**| Semantic    | Based on CodeBERT, GraphCodeBERT, and OpenAI embeddings       |

### CTSES Configurations

- **CTSES-AVG**: Uniform average (CodeBLEU + METEOR + ROUGE-L) / 3
- **CTSES-1**: (0.5 * CodeBLEU + 0.3 * METEOR + 0.2 * ROUGE-L)
- **CTSES-2**: (0.4 * CodeBLEU + 0.3 * METEOR + 0.3 * ROUGE-L)

---

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Then run the evaluation:

```bash
python3 evaluate_test_similarity.py
```

You should see output like the following:

```
====================================================================================================
EVALUATING LEXICAL AND STRUCTURAL SIMILARITY (CodeBLEU, METEOR, ROUGE-L, CTSES)
====================================================================================================
[CodeBLEU] Score                 : 0.4353
  - N-Gram Match                : 0.2532
  - Weighted N-Gram            : 0.4355
  - Syntax Match               : 0.6078
  - Dataflow Match             : 0.4444
[METEOR]                        : 0.6546
[ROUGE-L]                       : 0.5676
[CTSES - Average]               : 0.5525
[CTSES - (0.5, 0.3, 0.2)]       : 0.5275
[CTSES - (0.4, 0.3, 0.3)]       : 0.5408

====================================================================================================
EVALUATING SEMANTIC SIMILARITY (CodeBERT, GraphCodeBERT, OpenAI)
====================================================================================================
Cosine Similarity (CodeBERT)     : 0.9976
Cosine Similarity (GraphCodeBERT): 0.9909
Cosine Similarity (OpenAI)       : 0.9492
====================================================================================================
```

---

## Takeaways

- CTSES delivers more **balanced and faithful assessments** than individual metrics.
- It reduces **false negatives** that occur when CodeBLEU penalizes meaningful refactorings.
- Semantic similarity confirms behavior preservation, but CTSES adds readability and structure.

---

## References

- S. Ren et al., *CodeBLEU: a method for automatic evaluation of code synthesis*, arXiv:2009.10297.
- S. Banerjee and A. Lavie, *METEOR: An automatic metric for MT evaluation*, ACL Workshop 2005.
- C.-Y. Lin, *ROUGE: A package for automatic evaluation of summaries*, ACL 2004.
- Z. Feng et al., *CodeBERT: A pre-trained model for programming and natural languages*, arXiv:2002.08155.
- D. Guo et al., *GraphCodeBERT: Pre-training code representations with data flow*, arXiv:2009.08366.
