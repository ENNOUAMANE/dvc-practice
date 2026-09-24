import pandas as pd
import yaml
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Load parameters
with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)

test_size = params["train"]["test_size"]
random_state = params["train"]["random_state"]

# Load processed data
df = pd.read_csv("data/processed.csv")

X = df[["hours_studied"]]
y = df["passed"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=test_size,
    random_state=random_state,
    stratify=y
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "models/model.pkl")

# Save test data
test_df = X_test.copy()
test_df["passed"] = y_test.values
test_df.to_csv("data/test.csv", index=False)

# Save train data
train_df = X_train.copy()
train_df["passed"] = y_train.values
train_df.to_csv("data/train.csv", index=False)


print("Model trained and saved to models/model.pkl")
print("Train, Test data saved to data/train.csv and data/test.csv")