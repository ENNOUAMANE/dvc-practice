import pandas as pd

input_path = "data/dataset.csv"
output_path = "data/processed.csv"

df = pd.read_csv(input_path)

# Normalize hours_studied
for column in ["hours_studied", "attendance"]:
    min_value = df[column].min()
    max_value = df[column].max()

    df[column] = (
        (df[column] - min_value)
        / (max_value - min_value)
    )

df.to_csv(output_path, index=False)

print(f"Processed data saved to {output_path}")