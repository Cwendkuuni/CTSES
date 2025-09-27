import json
import os
import pandas as pd

# ============================
# Paths & configuration
# ============================
BASE_DIR = "/home/e113/Documents/Humanization-Project/HUMANIZATION/CODEBLEU-CRISTALBLEU/NEW-TESTS/NEW-FOR-ICSE-NIER-TRACK"
MODELS = ["GPT 4o", "MISTRAL LARGE"]
DATASETS = ["Defects4J", "SF110"]

N_PER_GROUP = 5

# Initial thresholds
DELTA_HIGH = 0.15
DELTA_LOW = -0.15
DELTA_MID = 0.05

# Relaxed thresholds if not enough cases
DELTA_HIGH_RELAX = 0.10
DELTA_LOW_RELAX = -0.10
DELTA_MID_RELAX = 0.10


# ============================
# Data loading & merging
# ============================
def load_and_merge(model, dataset):
    base_path = os.path.join(BASE_DIR, model)

    metrics_file = os.path.join(base_path, f"UPDATED_{dataset}-Scenario-1-metrics.json")
    pairs_file = os.path.join(base_path, f"{dataset}-Scenario-1-test-pairs.json")

    with open(metrics_file, "r") as f:
        metrics_data = json.load(f)
    with open(pairs_file, "r") as f:
        pairs_data = json.load(f)

    pairs_index = {
        (p["project_name"], p["class"], p["iteration_evosuite"], p["iteration_refactored"]): p
        for p in pairs_data
    }

    merged = []
    for m in metrics_data:
        key = (m["project_name"], m["class"], m["iteration_evosuite"], m["iteration_refactored"])
        if key in pairs_index:
            p = pairs_index[key]
            merged.append({
                "model": model,
                "dataset": dataset,
                "project_name": m["project_name"],
                "class": m["class"],
                "bug_id": m.get("bug-id"),
                "fqdn": m["fqdn"],
                "iteration_evosuite": m["iteration_evosuite"],
                "iteration_refactored": m["iteration_refactored"],
                "CodeBLEU": m["CodeBLEU"],
                "METEOR": m["METEOR"],
                "ROUGE-L": m["ROUGE-L"],
                "AVG": m["average_score_1"],          # Uniform average
                "CTSES1": m["CTSES_score_1"],         # Semantic-prioritized (0.5 / 0.3 / 0.2)
                "CTSES2": m["CTSES_score_2"],         # Readability-aware (0.4 / 0.3 / 0.3)
                "delta": m["CTSES_score_1"] - m["CodeBLEU"],  # Difference based on CTSES1
                "original_test": p["original_test"],
                "refactored_test": p["refactored_test"]
            })
    return merged


# ============================
# Selection strategy
# ============================
def select_group(df, group, n=N_PER_GROUP):
    if group == "G1":
        candidates = df[df["delta"] > DELTA_HIGH]
        if len(candidates) < n:
            candidates = df[df["delta"] > DELTA_HIGH_RELAX]
        if len(candidates) < n:
            candidates = df.sort_values("delta", ascending=False).head(n)
    elif group == "G2":
        candidates = df[df["delta"] < DELTA_LOW]
        if len(candidates) < n:
            candidates = df[df["delta"] < DELTA_LOW_RELAX]
        if len(candidates) < n:
            candidates = df.sort_values("delta", ascending=True).head(n)
    else:  # G3
        candidates = df[df["delta"].abs() <= DELTA_MID]
        if len(candidates) < n:
            candidates = df[df["delta"].abs() <= DELTA_MID_RELAX]
        if len(candidates) < n:
            candidates = df.iloc[:n]

    return candidates.sample(min(n, len(candidates)), random_state=42)


# ============================
# Main pipeline
# ============================
# Load all data
all_data = []
for model in MODELS:
    for dataset in DATASETS:
        all_data.extend(load_and_merge(model, dataset))

df = pd.DataFrame(all_data)
print(f"Total merged samples: {len(df)}")

# Representative selection
selected = pd.concat([
    select_group(df, "G1"),
    select_group(df, "G2"),
    select_group(df, "G3")
])

print(f"Selected {len(selected)} cases total.")

# Save as CSV and JSONL
out_csv = "selected_refactorings_15.csv"
out_jsonl = "selected_refactorings_15.jsonl"

selected.to_csv(out_csv, index=False)

with open(out_jsonl, "w") as f:
    for _, row in selected.iterrows():
        f.write(json.dumps(row.to_dict()) + "\n")

print(f"Saved {out_csv} and {out_jsonl}")
