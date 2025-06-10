import json
import pandas as pd
from pathlib import Path
import re

INPUT_DIR = Path(".")
OUTPUT_SUMMARY = "summary_stats_ctses_all_models.csv"
OUTPUT_AGGREGATED = "summary_stats_ctses_aggregated_by_dataset.csv"

# Columns to round and export
COLUMNS_TO_ROUND = [
    "Min", "Q1", "Median", "Q3", "Max", "Mean", "<0.5 %", ">=0.5 %"
]

def parse_model_and_dataset(filename):
    """Extract model and dataset from the file name using regex."""
    pattern = r"(GPT|MISTRAL)-STATS_(Defects4J|SF110)-Scenario-1-metrics\.json"
    match = re.match(pattern, filename)
    if not match:
        return None, None
    model_raw, dataset = match.groups()
    model_name = "GPT 4-o" if model_raw == "GPT" else "Mistral large-2407"
    return model_name, dataset

def load_metrics(file_path, model, dataset):
    """Load metrics from a single JSON file."""
    with open(file_path, "r") as f:
        data = json.load(f)

    records = []
    for metric, values in data.items():
        records.append({
            "Dataset": dataset,
            "Model": model,
            "Metric": metric,
            "Min": values.get("Min"),
            "Q1": values.get("Q1"),
            "Median": values.get("Median"),
            "Q3": values.get("Q3"),
            "Max": values.get("Max"),
            "Mean": values.get("Mean"),
            "<0.5 %": values.get("<0.5 %"),
            ">=0.5 %": values.get(">=0.5 %")
        })
    return records

def aggregate_metrics(records):
    """Aggregate metrics across models per dataset and metric."""
    df = pd.DataFrame(records)
    df = df[["Dataset", "Model", "Metric"] + COLUMNS_TO_ROUND]
    df[COLUMNS_TO_ROUND] = df[COLUMNS_TO_ROUND].round(2)

    df.to_csv(OUTPUT_SUMMARY, index=False)
    print(f"Summary exported to: {OUTPUT_SUMMARY}")

    df_agg = df.groupby(["Dataset", "Metric"])[COLUMNS_TO_ROUND].mean().reset_index()
    df_agg[COLUMNS_TO_ROUND] = df_agg[COLUMNS_TO_ROUND].round(2)
    df_agg.to_csv(OUTPUT_AGGREGATED, index=False)
    print(f"Aggregated summary exported to: {OUTPUT_AGGREGATED}")

def main():
    all_records = []
    for file_path in INPUT_DIR.glob("*.json"):
        model, dataset = parse_model_and_dataset(file_path.name)
        if not model or not dataset:
            continue
        records = load_metrics(file_path, model, dataset)
        all_records.extend(records)

    if all_records:
        aggregate_metrics(all_records)
    else:
        print("No valid metric files found.")

if __name__ == "__main__":
    main()
