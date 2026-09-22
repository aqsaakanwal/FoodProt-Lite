import os
import pandas as pd


RAW_FILE = os.path.join("data", "raw", "food_protein_raw.csv")
PROCESSED_DIR = os.path.join("data", "processed")
REPORTS_DIR = "reports"

PROCESSED_FILE = os.path.join(
    PROCESSED_DIR,
    "food_protein_standardized.csv"
)

QUALITY_REPORT_FILE = os.path.join(
    REPORTS_DIR,
    "data_quality_report.csv"
)


# ---------------------------------------------------------
# Load raw dataset
# ---------------------------------------------------------

df = pd.read_csv(RAW_FILE)

print("Raw dataset loaded.")
print(f"Initial rows: {len(df)}")
print(f"Initial columns: {len(df.columns)}")


# ---------------------------------------------------------
# Standardize column names
# ---------------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# ---------------------------------------------------------
# Record data quality information before cleaning
# ---------------------------------------------------------

rows_before = len(df)

duplicate_rows_before = df.duplicated().sum()

missing_before = int(df.isna().sum().sum())


# ---------------------------------------------------------
# Remove exact duplicate rows
# ---------------------------------------------------------

df = df.drop_duplicates().reset_index(drop=True)

rows_after_duplicates = len(df)


# ---------------------------------------------------------
# Basic numerical validity checks
# ---------------------------------------------------------

# pH should normally be between 0 and 14
if "pH" in df.columns:
    df.loc[
        (df["pH"] < 0) | (df["pH"] > 14),
        "pH"
    ] = pd.NA


# Temperature validity check
if "temperature_c" in df.columns:
    df.loc[
        (df["temperature_c"] < -20) |
        (df["temperature_c"] > 200),
        "temperature_c"
    ] = pd.NA


# Protein concentration should be positive
if "protein_concentration_pct" in df.columns:
    df.loc[
        df["protein_concentration_pct"] <= 0,
        "protein_concentration_pct"
    ] = pd.NA


# ---------------------------------------------------------
# Fill missing numerical values using median
# ---------------------------------------------------------

numerical_columns = df.select_dtypes(
    include=["number"]
).columns

for column in numerical_columns:

    if df[column].isna().any():
        median_value = df[column].median()

        df[column] = df[column].fillna(median_value)


# ---------------------------------------------------------
# Fill missing categorical values
# ---------------------------------------------------------

categorical_columns = df.select_dtypes(
    include=["object"]
).columns

for column in categorical_columns:

    df[column] = df[column].fillna("Unknown")


# ---------------------------------------------------------
# Remove completely empty rows if any
# ---------------------------------------------------------

df = df.dropna(how="all").reset_index(drop=True)


# ---------------------------------------------------------
# Final data-quality information
# ---------------------------------------------------------

rows_after_cleaning = len(df)

missing_after = int(df.isna().sum().sum())

duplicate_rows_after = df.duplicated().sum()


# ---------------------------------------------------------
# Create directories
# ---------------------------------------------------------

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


# ---------------------------------------------------------
# Save standardized dataset
# ---------------------------------------------------------

df.to_csv(
    PROCESSED_FILE,
    index=False
)


# ---------------------------------------------------------
# Create data-quality report
# ---------------------------------------------------------

quality_report = pd.DataFrame({
    "metric": [
        "Rows before cleaning",
        "Duplicate rows detected",
        "Rows after duplicate removal",
        "Missing values before cleaning",
        "Missing values after cleaning",
        "Duplicate rows after cleaning",
        "Final rows",
        "Final columns",
    ],
    "value": [
        rows_before,
        duplicate_rows_before,
        rows_after_duplicates,
        missing_before,
        missing_after,
        duplicate_rows_after,
        rows_after_cleaning,
        len(df.columns),
    ]
})


quality_report.to_csv(
    QUALITY_REPORT_FILE,
    index=False
)


# ---------------------------------------------------------
# Print summary
# ---------------------------------------------------------

print("\nData cleaning completed successfully.")

print(f"Rows before cleaning: {rows_before}")
print(f"Duplicate rows detected: {duplicate_rows_before}")
print(f"Rows after duplicate removal: {rows_after_duplicates}")
print(f"Missing values before cleaning: {missing_before}")
print(f"Missing values after cleaning: {missing_after}")
print(f"Final rows: {rows_after_cleaning}")
print(f"Final columns: {len(df.columns)}")

print("\nStandardized dataset saved to:")
print(PROCESSED_FILE)

print("\nData-quality report saved to:")
print(QUALITY_REPORT_FILE)
