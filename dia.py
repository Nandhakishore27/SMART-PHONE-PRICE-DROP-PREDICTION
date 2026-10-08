import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("Telco-Customer-Churn.csv")

# -----------------------------
# Data Preprocessing
# -----------------------------

# Drop unnecessary column
df = df.drop("customerID", axis=1)

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# Remove missing values
df = df.dropna()

# Convert target to binary
df["Churn"] = df["Churn"].map({"No": 0, "Yes": 1})

# Convert categorical → numeric
df = pd.get_dummies(df, drop_first=True)

# -----------------------------
# Features & Target
# -----------------------------
X = df.drop("Churn", axis=1)
y = df["Churn"]

# -----------------------------
# Train Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=0
)

# -----------------------------
# Train Model
# -----------------------------
model = RandomForestClassifier()
model.fit(X_train, y_train)

# -----------------------------
# Accuracy
# -----------------------------
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))

# -----------------------------
# Save Model + Columns (IMPORTANT)
# -----------------------------
with open("churn_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("columns.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("Model saved successfully!")