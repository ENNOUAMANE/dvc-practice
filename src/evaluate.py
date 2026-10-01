import json
import os
import pandas as pd
import joblib
import yaml

from sklearn.metrics import accuracy_score

# Load parameters
with open("params.yaml", "r") as f:
    params = yaml.safe_load(f)

test_size = params["train"]["test_size"]

# Load test data
test_df = pd.read_csv("data/test.csv")

X_test = test_df[["hours_studied", "attendance"]]
y_test = test_df["passed"]

# Load trained model
model = joblib.load("models/model.pkl")

# Make predictions
predictions = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, predictions)

# Save metrics
metrics = {
    "accuracy": accuracy
}

with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

# Save data for DVC plot
os.makedirs("plots", exist_ok=True)

plot_data = pd.DataFrame({
    "test_size": [test_size],
    "accuracy": [accuracy]
})

plot_data.to_csv("plots/accuracy.csv", index=False)

print(f"Accuracy: {accuracy:.4f}")
print("Metrics saved to metrics.json")
print("Plot data saved to plots/accuracy.csv")