# Developer-Aligned Validation

This directory contains all artifacts, scripts, and results related to the **human-centered validation** of CTSES.  
It complements the large-scale evaluation by directly comparing metric scores with developer annotations.

---

## Contents

- **`DevA_annotations_clean_exact.xlsx`**  
  Annotations from Developer A (senior engineer).  
- **`DevB_annotations_clean_exact.xlsx`**  
  Annotations from Developer B (PhD student).  
- **`DevC_annotations_clean_exact.xlsx`**  
  Annotations from Developer C (junior assistant).  
- **`DevX_annotations_Empty.xlsx`**  
  Empty annotation template provided to developers (includes metadata and fields for clarity/behavior judgments).  
- **`consolidated_annotations_clean.xlsx`**  
  Consensus annotations (majority vote) with aligned metric scores.  
- **`selected_refactorings_15.jsonl` / `selected_refactorings_15.csv`**  
  Subset of 15 representative refactorings sampled from Defects4J and SF110 for validation.  
- **`SF110_XPathLexer_iter-2.jsonl`**  
  Case study example (false negative) highlighted in the paper.  
- **`CSV_Version/`**  
  Contains equivalent `.csv` versions of all Excel files for easier parsing:
  - `DevA_annotations_clean_exact.csv`  
  - `DevB_annotations_clean_exact.csv`  
  - `DevC_annotations_clean_exact.csv`  
  - `DevX_annotations_Empty.csv`  
  - `consolidated_annotations_clean.csv`  
  - `mae_fn_simple.csv`  
  - `ctses_gridsearch_results.csv`  

---

## Scripts

- **`select_tests_human_evalaution.py`**  
  Script used to select representative test pairs for annotation.  
- **`analyse_human_evaluation.py`**  
  Computes MAE and false negatives by comparing metric scores against developer consensus.  
- **`ctses_gridsearch_empirical.py`**  
  Runs a grid search over CTSES weights `(α, β, γ)` to evaluate empirical trade-offs.  
- **`get_consolidated_annotations.py`**  
  Builds the consensus file by merging developer annotations (A, B, C) using majority vote.

---

## Results

- **`mae_fn_simple.xlsx`**  
  Raw results of MAE and false negatives for each metric (CodeBLEU, AVG, CTSES1, CTSES2).  
- **`ctses_gridsearch_results.xlsx`**  
  Grid search output ranking configurations by MAE and FN count.  

---

## Usage

1. **Run consensus analysis (MAE + FN):**
   ```bash
   python3 analyse_human_evaluation.py
   ```

2. **Reproduce weight grid search:**
   ```bash
   python3 ctses_gridsearch_empirical.py
   ```

3. **Rebuild consolidated annotations from developer files:**
   ```bash
   python3 get_consolidated_annotations.py
   ```

---

## Notes

- Three developers annotated all 15 refactorings independently.  
- Consensus was derived by majority vote (2/3).  
- Both `.xlsx` and `.csv` formats are provided for flexibility.  
- Annotations, scripts, and results are released to ensure full transparency and replicability.  
- These artifacts support Section *Developer-Aligned Validation* in the paper.
