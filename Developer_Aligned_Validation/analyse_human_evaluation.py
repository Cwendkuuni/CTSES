import pandas as pd
import numpy as np

# Charger le fichier consolidé
df = pd.read_excel("consolidated_annotations_clean.xlsx", sheet_name="Consolidated")

# Utiliser la colonne "key" comme identifiant unique
id_col = "key"
df = df.drop_duplicates(subset=[id_col], keep="first")

# Labels humains (Yes=1, No=0)
y_true = df["Clarity_Improved_A"].map({"Yes": 1, "No": 0}).astype(float)

# Scores des métriques
metrics = ["CodeBLEU", "AVG", "CTSES1", "CTSES2"]

results = []

for metric in metrics:
    if metric in df.columns:
        scores = df[metric].astype(float)

        # MAE continu
        mae = np.mean(np.abs(y_true - scores))

        # False Negatives : y=1 mais score<0.5
        fn_keys = df.loc[(y_true == 1) & (scores < 0.5), id_col].tolist()
        fn_count = len(fn_keys)

        results.append({
            "Metric": metric,
            "MAE_Continuous": round(mae, 6),
            "FN@0.5_Count": fn_count,
            "FN@0.5_Keys": ",".join(map(str, fn_keys)) if fn_keys else "-"
        })

# Résultats
results_df = pd.DataFrame(results)

print("📊 Résultats (basés sur consolidated_annotations_clean.xlsx):")
print(results_df)

# Sauvegarde
results_df.to_excel("mae_fn_simple.xlsx", index=False)
print("\n✅ Saved: mae_fn_simple.xlsx")

