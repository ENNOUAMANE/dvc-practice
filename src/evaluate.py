import json
import pandas as pd
import joblib

from sklearn.metrics import accuracy_score

# Load test data
test_df = pd.read_csv("data/test.csv")

X_test = test_df[["hours_studied"]]
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

print(f"Accuracy: {accuracy:.4f}")
print("Metrics saved to metrics.json")