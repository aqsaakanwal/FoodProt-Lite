import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

DATA_FILE = os.path.join(
    "data",
    "processed",
    "food_protein_standardized.csv"
)

MODEL_DIR = "models"
REPORTS_DIR = "reports"

MODEL_FILE = os.path.join(
    MODEL_DIR,
    "functionality_model.pkl"
)

METRICS_FILE = os.path.join(
    REPORTS_DIR,
    "model_metrics.csv"
)


# ---------------------------------------------------------
# Load standardized dataset
# ---------------------------------------------------------

df = pd.read_csv(DATA_FILE)

print("Standardized dataset loaded.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ---------------------------------------------------------
# Define target and features
# ---------------------------------------------------------

target = "solubility_pct"

features = [
    "protein_source",
    "protein_category",
    "ph",
    "temperature_c",
    "protein_concentration_pct",
    "processing_method",
    "extraction_method",
]

X = df[features]
y = df[target]


# ---------------------------------------------------------
# Identify categorical and numerical features
# ---------------------------------------------------------

categorical_features = [
    "protein_source",
    "protein_category",
    "processing_method",
    "extraction_method",
]

numerical_features = [
    "ph",
    "temperature_c",
    "protein_concentration_pct",
]


# ---------------------------------------------------------
# Preprocessing
# ---------------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features,
        ),
        (
            "numerical",
            "passthrough",
            numerical_features,
        ),
    ]
)


# ---------------------------------------------------------
# Random Forest model
# ---------------------------------------------------------

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=8,
    min_samples_leaf=2,
    random_state=42,
)


# ---------------------------------------------------------
# Complete ML pipeline
# ---------------------------------------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model),
    ]
)


# ---------------------------------------------------------
# Train-test split
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
)


print(f"\nTraining records: {len(X_train)}")
print(f"Testing records: {len(X_test)}")


# ---------------------------------------------------------
# Train model
# ---------------------------------------------------------

pipeline.fit(X_train, y_train)


# ---------------------------------------------------------
# Generate predictions
# ---------------------------------------------------------

predictions = pipeline.predict(X_test)


# ---------------------------------------------------------
# Calculate evaluation metrics
# ---------------------------------------------------------

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)


# ---------------------------------------------------------
# Save model
# ---------------------------------------------------------

os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(
    pipeline,
    MODEL_FILE
)


# ---------------------------------------------------------
# Save model metrics
# ---------------------------------------------------------

os.makedirs(REPORTS_DIR, exist_ok=True)

metrics = pd.DataFrame({
    "metric": [
        "MAE",
        "RMSE",
        "R2"
    ],
    "value": [
        round(mae, 4),
        round(rmse, 4),
        round(r2, 4)
    ]
})

metrics.to_csv(
    METRICS_FILE,
    index=False
)


# ---------------------------------------------------------
# Print results
# ---------------------------------------------------------

print("\nModel training completed successfully.")

print(f"MAE: {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R2: {r2:.4f}")

print("\nModel saved to:")
print(MODEL_FILE)

print("\nModel metrics saved to:")
print(METRICS_FILE)
