import pandas as pd

# Load Excel files
devA = pd.read_excel("DevA_annotations_clean_exact.xlsx")
devB = pd.read_excel("DevB_annotations_clean_exact.xlsx")
devC = pd.read_excel("DevC_annotations_clean_exact.xlsx")

# Merge while keeping annotator-specific columns
merged = devA.merge(
    devB[["key", "Clarity_Improved_B", "Behavior_Preserved_B", "Comment_B"]],
    on="key", how="outer"
).merge(
    devC[["key", "Clarity_Improved_C", "Behavior_Preserved_C", "Comment_C"]],
    on="key", how="outer"
)

# Save consolidated results
merged.to_excel("consolidated_annotations_clean.xlsx", index=False)
merged.to_csv("consolidated_annotations_clean.csv", index=False)

print("Consolidation completed: consolidated_annotations_clean.xlsx / .csv generated")
