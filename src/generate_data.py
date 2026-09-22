import os
import numpy as np
import pandas as pd

SEED = 42
N_RECORDS = 250

np.random.seed(SEED)

# Protein sources
protein_sources = [
    ("Pea Protein", "Pea", "Plant"),
    ("Soy Protein", "Soy", "Plant"),
    ("Mung Bean Protein", "Mung Bean", "Plant"),
    ("Rice Protein", "Rice", "Plant"),
    ("Chickpea Protein", "Chickpea", "Plant"),
    ("Potato Protein", "Potato", "Plant"),
    ("Hemp Protein", "Hemp", "Plant"),
    ("Spirulina Protein", "Spirulina", "Algae"),
]

processing_methods = [
    "Untreated",
    "Heat",
    "pH Shift",
    "High Pressure"
]

extraction_methods = [
    "Alkaline Extraction",
    "Salt Extraction",
    "Aqueous Extraction"
]

measurement_methods = [
    "Spectrophotometric",
    "Emulsion Test",
    "Foam Test",
    "Texture Analysis"
]

rows = []

for i in range(N_RECORDS):

    protein_name, protein_source, protein_category = protein_sources[
        np.random.randint(len(protein_sources))
    ]

    processing = np.random.choice(processing_methods)
    extraction = np.random.choice(extraction_methods)
    measurement = np.random.choice(measurement_methods)

    pH = round(np.random.uniform(4.5, 9.0), 2)
    temperature = round(np.random.uniform(20, 90), 1)
    concentration = round(np.random.uniform(2, 10), 2)

    # Small synthetic effects for demonstration only
    protein_effect = {
        "Pea": 4,
        "Soy": 7,
        "Mung Bean": 3,
        "Rice": 1,
        "Chickpea": 2,
        "Potato": 5,
        "Hemp": 0,
        "Spirulina": 6,
    }[protein_source]

    processing_effect = {
        "Untreated": 0,
        "Heat": 4,
        "pH Shift": 6,
        "High Pressure": 8,
    }[processing]

    extraction_effect = {
        "Alkaline Extraction": 5,
        "Salt Extraction": 2,
        "Aqueous Extraction": 0,
    }[extraction]

    # Synthetic functionality measurements
    solubility = (
        45
        + protein_effect
        + processing_effect
        + extraction_effect
        + 7 * np.exp(-((pH - 7) ** 2) / 2)
        - 0.08 * abs(temperature - 50)
        - 0.5 * concentration
        + np.random.normal(0, 3)
    )

    emulsification = (
        50
        + protein_effect * 0.8
        + 5 * np.exp(-((pH - 7) ** 2) / 2)
        + np.random.normal(0, 4)
    )

    foaming = (
        40
        + protein_effect * 0.7
        + (10 if processing == "High Pressure" else 0)
        + np.random.normal(0, 5)
    )

    gel_strength = (
        35
        + protein_effect
        + processing_effect * 1.5
        + 0.25 * temperature
        + np.random.normal(0, 6)
    )

    # Keep synthetic measurements within reasonable demonstration ranges
    solubility = np.clip(solubility, 5, 100)
    emulsification = np.clip(emulsification, 5, 100)
    foaming = np.clip(foaming, 5, 100)
    gel_strength = np.clip(gel_strength, 5, 150)

    rows.append({
        "record_id": i + 1,
        "protein_name": protein_name,
        "protein_source": protein_source,
        "protein_category": protein_category,
        "pH": pH,
        "temperature_c": temperature,
        "protein_concentration_pct": concentration,
        "processing_method": processing,
        "extraction_method": extraction,
        "measurement_method": measurement,
        "solubility_pct": round(solubility, 2),
        "emulsification_index": round(emulsification, 2),
        "foaming_capacity_pct": round(foaming, 2),
        "gel_strength_g": round(gel_strength, 2),
    })

df = pd.DataFrame(rows)

# ---------------------------------------------------------
# Introduce a small number of missing values intentionally
# so the cleaning pipeline can demonstrate data-quality work.
# ---------------------------------------------------------

missing_locations = [
    (10, "pH"),
    (25, "temperature_c"),
    (40, "protein_concentration_pct"),
    (55, "processing_method"),
    (70, "extraction_method"),
    (85, "solubility_pct"),
    (100, "emulsification_index"),
    (115, "foaming_capacity_pct"),
    (130, "gel_strength_g"),
    (145, "protein_source"),
    (160, "measurement_method"),
    (175, "protein_category"),
]

for row_index, column in missing_locations:
    df.loc[row_index, column] = np.nan

# Add 3 duplicate records intentionally
duplicates = df.iloc[[5, 50, 100]].copy()
df = pd.concat([df, duplicates], ignore_index=True)

# Create output directory
output_path = os.path.join("data", "raw")
os.makedirs(output_path, exist_ok=True)

# Save raw synthetic dataset
file_path = os.path.join(output_path, "food_protein_raw.csv")
df.to_csv(file_path, index=False)

print(f"Dataset created successfully: {file_path}")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print("\nMissing values:")
print(df.isna().sum())
