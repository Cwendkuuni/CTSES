import pandas as pd
import numpy as np
import itertools

# Load the consolidated file
df = pd.read_excel("consolidated_annotations_clean.xlsx", sheet_name="Consolidated")

# Human labels (Yes=1, No=0)
y_true = df["Clarity_Consensus"].map({"Yes": 1, "No": 0}).astype(float)

# Retrieve the three base metrics
codebleu = df["CodeBLEU"].astype(float).values
meteor = df["METEOR"].astype(float).values
rouge = df["ROUGE-L"].astype(float).values

results = []

# Grid search with step size 0.1
steps = np.arange(0, 1.1, 0.1)
for alpha, beta, gamma in itertools.product(steps, steps, steps):
    if abs(alpha + beta + gamma - 1.0) > 1e-6:
        continue
    
    # Compute CTSES for this configuration
    scores = alpha * codebleu + beta * meteor + gamma * rouge
    
    # Continuous MAE
    mae = np.mean(np.abs(y_true - scores))
    
    # FN@0.5 (cases where y=1 but score < 0.5)
    fn_keys = df.loc[(y_true == 1) & (scores < 0.5), "key"].tolist()
    fn_count = len(fn_keys)
    
    results.append({
        "alpha": round(alpha, 2),
        "beta": round(beta, 2),
        "gamma": round(gamma, 2),
        "MAE": round(mae, 4),
        "FN@0.5": fn_count,
        "FN_Keys": ",".join(fn_keys)
    })

# Results sorted by ascending MAE then FN
results_df = pd.DataFrame(results).sort_values(by=["MAE", "FN@0.5"]).reset_index(drop=True)

print("Top 10 configurations (sorted by MAE then FN):")
print(results_df.head(10))

# Save complete results
results_df.to_excel("ctses_gridsearch_results.xlsx", index=False)
print("Saved: ctses_gridsearch_results.xlsx")
