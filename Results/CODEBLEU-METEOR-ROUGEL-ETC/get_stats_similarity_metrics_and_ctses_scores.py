import json
import pandas as pd
import numpy as np
from pathlib import Path

# Paths and config
INPUT_DIR = Path(".")
OUTPUT_DIR = Path("ctses_stats_outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# Mapping of source files
FILES = {
    "GPT-Defects4J": INPUT_DIR / "GPT-UPDATED_Defects4J-Scenario-1-metrics.json",
    "GPT-SF110": INPUT_DIR / "GPT-UPDATED_SF110-Scenario-1-metrics.json",
    "MISTRAL-Defects4J": INPUT_DIR / "MISTRAL-UPDATED_Defects4J-Scenario-1-metrics.json",
    "MISTRAL-SF110": INPUT_DIR / "MISTRAL-UPDATED_SF110-Scenario-1-metrics.json",
}

SIMILARITY_METRICS = [
    "METEOR", "ROUGE-L", "CodeBLEU", "N-gram Match",
    "Weighted N-gram Match", "Syntax Match", "Dataflow Match"
]
CTSES_METRICS = [
    "average_score_1", "CTSES_score_1", "CTSES_score_2"
]

def load_data():
    """Load and normalize JSON input files into a DataFrame."""
    records = []
    for label, path in FILES.items():
        model_key, dataset = label.split("-")
        model = "GPT 4-o" if model_key == "GPT" else "Mistral large-2407"

        with open(path, "r") as f:
            data = json.load(f)
            for entry in data:
                record = {
                    "Model": model,
                    "Dataset": dataset,
                }
                for metric in SIMILARITY_METRICS + CTSES_METRICS:
                    record[metric] = entry.get(metric)
                records.append(record)
    return pd.DataFrame(records)

def compute_stats(df, group_cols, metrics):
    """Compute summary statistics per group for the specified metrics."""
    stats = []
    for metric in metrics:
        grouped = df.groupby(group_cols)[metric].agg([
            ('Min', 'min'),
            ('Q1', lambda x: np.percentile(x.dropna(), 25)),
            ('Median', 'median'),
            ('Q3', lambda x: np.percentile(x.dropna(), 75)),
            ('Max', 'max'),
            ('Mean', 'mean')
        ]).reset_index()
        grouped["Metric"] = metric
        stats.append(grouped)
    return pd.concat(stats, ignore_index=True)

def compute_global_stats(df, metrics):
    """Compute overall statistics for the specified metrics (across all models and datasets)."""
    global_stats = []
    for metric in metrics:
        values = df[metric].dropna()
        global_stats.append({
            "Metric": metric,
            "Min": values.min(),
            "Q1": np.percentile(values, 25),
            "Median": np.median(values),
            "Q3": np.percentile(values, 75),
            "Max": values.max(),
            "Mean": values.mean()
        })
    return pd.DataFrame(global_stats)

def export_dataframe(df, filename):
    """Save the given DataFrame to CSV in the output directory."""
    output_path = OUTPUT_DIR / filename
    df.to_csv(output_path, index=False)
    print(f"- {output_path.name}")

def main():
    df = load_data()

    print("Generating grouped statistics...")
    similarity_stats = compute_stats(df, ["Dataset", "Model"], SIMILARITY_METRICS)
    ctses_stats = compute_stats(df, ["Dataset", "Model"], CTSES_METRICS)

    similarity_stats = similarity_stats[["Dataset", "Model", "Metric", "Min", "Q1", "Median", "Q3", "Max", "Mean"]]
    ctses_stats = ctses_stats[["Dataset", "Model", "Metric", "Min", "Q1", "Median", "Q3", "Max", "Mean"]]

    export_dataframe(similarity_stats, "stats_similarity_metrics.csv")
    export_dataframe(ctses_stats, "stats_ctses_scores.csv")

    print("Generating global statistics...")
    global_similarity = compute_global_stats(df, SIMILARITY_METRICS)
    global_ctses = compute_global_stats(df, CTSES_METRICS)

    export_dataframe(global_similarity, "global_stats_similarity_metrics.csv")
    export_dataframe(global_ctses, "global_stats_ctses_scores.csv")

if __name__ == "__main__":
    main()
