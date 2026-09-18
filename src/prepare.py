import pandas as pd

input_path = "data/dataset.csv"
output_path = "data/processed.csv"

df = pd.read_csv(input_path)

# Normalize hours_studied to the range [0, 1]
min_hours = df["hours_studied"].min()
max_hours = df["hours_studied"].max()

df["hours_studied"] = (
    (df["hours_studied"] - min_hours)
    / (max_hours - min_hours)
)

df.to_csv(output_path, index=False)

print(f"Processed data saved to {output_path}")