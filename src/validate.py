import pandas as pd

input_path = "data/dataset.csv"
output_path = "data/validated.csv"

# Load dataset
df = pd.read_csv(input_path)

# 1. Check required columns
required_columns = ["hours_studied", "attendance", "passed"]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

# 2. Check that the dataset is not empty
if df.empty:
    raise ValueError("Dataset is empty.")

# 3. Ensure required columns contain numeric values
for column in required_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# 4. Check for missing or non-numeric values
if df[required_columns].isnull().any().any():
    raise ValueError("Dataset contains missing or non-numeric values.")

# 5. Check valid ranges
if (df["hours_studied"] <= 0).any():
    raise ValueError("hours_studied must be greater than 0.")

if not df["attendance"].between(0, 100).all():
    raise ValueError("attendance must be between 0 and 100.")

if not df["passed"].isin([0, 1]).all():
    raise ValueError("passed must contain only 0 or 1.")

# 6. Check both classes have enough samples
class_counts = df["passed"].value_counts()

for label in [0, 1]:
    if class_counts.get(label, 0) < 2:
        raise ValueError(
            f"Class {label} needs at least 2 samples."
        )

# 7. Prevent division by zero during normalization
for column in ["hours_studied", "attendance"]:
    if df[column].nunique() < 2:
        raise ValueError(
            f"{column} must have at least 2 distinct values."
        )

# Save validated data for the next stage
df.to_csv(output_path, index=False)

print("Dataset validation passed.")
print(f"Validated data saved to {output_path}")
print(f"Dataset contains {len(df)} rows.")