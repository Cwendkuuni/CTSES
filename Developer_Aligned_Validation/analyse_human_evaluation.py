# analyse_human_evaluation.py
import pandas as pd
import numpy as np
import os

SRC_XLSX = "consolidated_annotations_clean.xlsx"
SRC_CSV  = "consolidated_annotations_clean.csv"
OUT_XLSX = "mae_fn_simple.xlsx"

def load_consolidated():
    if os.path.exists(SRC_XLSX):
        # Read all sheets and choose intelligently
        sheets = pd.read_excel(SRC_XLSX, sheet_name=None)
        if "Consolidated" in sheets:
            df = sheets["Consolidated"]
            used = "Excel:Consolidated"
        else:
            # Take the first available sheet
            first_name = list(sheets.keys())[0]
            df = sheets[first_name]
            used = f"Excel:{first_name}"
    elif os.path.exists(SRC_CSV):
        df = pd.read_csv(SRC_CSV)
        used = "CSV"
    else:
        raise FileNotFoundError(f"Cannot find {SRC_XLSX} or {SRC_CSV}")
    return df, used

def to_float(series):
    return pd.to_numeric(series, errors="coerce").astype(float)

def normalize_yes_no(s):
    if pd.isna(s):
        return np.nan
    s = str(s).strip().lower()
    if s in ["yes", "oui", "y", "1", "true"]:
        return "Yes"
    if s in ["no", "non", "n", "0", "false"]:
        return "No"
    return np.nan

def majority_vote_yes_no(row, cols):
    vals = [normalize_yes_no(row[c]) for c in cols if c in row.index]
    vals = [v for v in vals if v in ["Yes", "No"]]
    if not vals:
        return np.nan
    yes = sum(v == "Yes" for v in vals)
    no  = sum(v == "No"  for v in vals)
    if yes > no:
        return "Yes"
    if no > yes:
        return "No"
    # Tie case -> default to No for safety
    return "No"

def main():
    df, used_src = load_consolidated()

    # Unique key
    id_col = "key" if "key" in df.columns else ("ID" if "ID" in df.columns else None)
    if id_col is None:
        raise KeyError("No identifier column found (expected: 'key' or 'ID').")
    df = df.drop_duplicates(subset=[id_col], keep="first").copy()

    # Ensure AVG is present if not already
    if "AVG" not in df.columns:
        needed = ["CodeBLEU", "METEOR", "ROUGE-L"]
        if all(col in df.columns for col in needed):
            df["AVG"] = (to_float(df["CodeBLEU"]) + to_float(df["METEOR"]) + to_float(df["ROUGE-L"])) / 3.0

    # Determine human labels (priority: consensus > majority vote > annotator A)
    label_source = None
    if "Clarity_Consensus" in df.columns:
        y_col = "Clarity_Consensus"
        label_source = "Clarity_Consensus"
    else:
        vote_cols = [c for c in df.columns if c.startswith("Clarity_Improved_")]
        if len(vote_cols) >= 2:
            df["Clarity_Majority"] = df.apply(lambda r: majority_vote_yes_no(r, vote_cols), axis=1)
            y_col = "Clarity_Majority"
            label_source = f"majority({','.join(vote_cols)})"
        elif "Clarity_Improved_A" in df.columns:
            y_col = "Clarity_Improved_A"
            label_source = "Clarity_Improved_A"
        else:
            raise KeyError("No human label column found (Clarity_Consensus / Clarity_Improved_*).")

    y_true = df[y_col].map({"Yes": 1, "No": 0}).astype(float)

    # Candidate metrics (only keep those present in the dataframe)
    candidates = ["CodeBLEU", "AVG", "CTSES1", "CTSES2"]
    metrics = [m for m in candidates if m in df.columns]

    results = []
    for metric in metrics:
        scores = to_float(df[metric])

        # MAE
        mae = float(np.nanmean(np.abs(y_true - scores)))

        # False negatives @ 0.5
        fn_mask = (y_true == 1) & (scores < 0.5)
        fn_keys = df.loc[fn_mask, id_col].astype(str).tolist()

        results.append({
            "Metric": metric,
            "MAE_Continuous": round(mae, 6),
            "FN@0.5_Count": len(fn_keys),
            "FN@0.5_Keys": ",".join(fn_keys) if fn_keys else "-"
        })

    results_df = pd.DataFrame(results).sort_values(by=["MAE_Continuous", "FN@0.5_Count"]).reset_index(drop=True)

    print(f"Source file: {used_src}")
    print(f"Human label source: {label_source}")
    print("\nResults (based on 15 unique rows):")
    print(results_df)

    results_df.to_excel(OUT_XLSX, index=False)
    print(f"\nSaved: {OUT_XLSX}")

if __name__ == "__main__":
    main()
