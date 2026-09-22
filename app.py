import os

import joblib
import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="FoodProt-Lite",
    page_icon="🧪",
    layout="wide",
)


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

DATA_FILE = os.path.join(
    "data",
    "processed",
    "food_protein_standardized.csv"
)

MODEL_FILE = os.path.join(
    "models",
    "functionality_model.pkl"
)

QUALITY_REPORT_FILE = os.path.join(
    "reports",
    "data_quality_report.csv"
)

METRICS_FILE = os.path.join(
    "reports",
    "model_metrics.csv"
)


# ---------------------------------------------------------
# Load data and model
# ---------------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)


@st.cache_data
def load_quality_report():
    return pd.read_csv(QUALITY_REPORT_FILE)


@st.cache_data
def load_metrics():
    return pd.read_csv(METRICS_FILE)


@st.cache_resource
def load_model():
    return joblib.load(MODEL_FILE)


# ---------------------------------------------------------
# Check required files
# ---------------------------------------------------------

required_files = [
    DATA_FILE,
    MODEL_FILE,
    QUALITY_REPORT_FILE,
    METRICS_FILE,
]

missing_files = [
    file for file in required_files
    if not os.path.exists(file)
]


if missing_files:

    st.error(
        "Some project files are missing. "
        "Please run the data-generation, cleaning, "
        "and model-training scripts first."
    )

    for file in missing_files:
        st.write(f"- {file}")

    st.stop()


df = load_data()
quality_report = load_quality_report()
metrics = load_metrics()
model = load_model()


# ---------------------------------------------------------
# Title
# ---------------------------------------------------------

st.title("🧪 FoodProt-Lite")

st.subheader(
    "Food Protein Functionality Data Explorer"
)

st.info(
    "FoodProt-Lite is an independent educational prototype "
    "inspired by data-standardization and predictive-modeling "
    "challenges in food protein research. "
    "It is not the official FoodProt platform and is not "
    "affiliated with San Diego State University."
)


# ---------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a section:",
    [
        "Overview",
        "Data Quality",
        "Explore Data",
        "Prediction",
        "Model Evaluation",
    ],
)


# =========================================================
# 1. OVERVIEW
# =========================================================

if page == "Overview":

    st.header("Project Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Records",
        len(df)
    )

    col2.metric(
        "Variables",
        len(df.columns)
    )

    col3.metric(
        "Protein Sources",
        df["protein_source"].nunique()
    )

    col4.metric(
        "Processing Methods",
        df["processing_method"].nunique()
    )

    st.markdown("---")

    st.subheader("Research Question")

    st.write(
        "How can fragmented food-protein functionality "
        "information be organized into a structured dataset "
        "and then used for exploratory analysis and basic "
        "machine learning?"
    )

    st.subheader("Workflow")

    st.markdown(
        """
        **Synthetic Data**
        → **Data Cleaning**
        → **Standardization**
        → **Data Quality Assessment**
        → **Exploratory Analysis**
        → **Machine Learning**
        → **Solubility Prediction**
        """
    )

    st.subheader("Protein Sources")

    protein_counts = (
        df["protein_source"]
        .value_counts()
        .reset_index()
    )

    protein_counts.columns = [
        "protein_source",
        "count",
    ]

    fig = px.bar(
        protein_counts,
        x="protein_source",
        y="count",
        title="Records by Protein Source",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.warning(
        "Scientific note: The current dataset is synthetic "
        "and is intended only for educational demonstration. "
        "The predictions should not be interpreted as "
        "experimentally validated scientific results."
    )


# =========================================================
# 2. DATA QUALITY
# =========================================================

elif page == "Data Quality":

    st.header("Data Quality Dashboard")

    final_rows = len(df)
    missing_values = int(df.isna().sum().sum())
    duplicates = int(df.duplicated().sum())

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Final Records",
        final_rows
    )

    col2.metric(
        "Missing Values",
        missing_values
    )

    col3.metric(
        "Duplicate Rows",
        duplicates
    )

    st.subheader("Cleaning Report")

    st.dataframe(
        quality_report,
        use_container_width=True,
    )

    st.subheader("Missing Values by Variable")

    missing_by_column = (
        df.isna()
        .sum()
        .reset_index()
    )

    missing_by_column.columns = [
        "variable",
        "missing_values",
    ]

    fig = px.bar(
        missing_by_column,
        x="variable",
        y="missing_values",
        title="Missing Values After Cleaning",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader("Dataset Completeness")

    completeness = (
        100
        - (
            df.isna().sum().sum()
            / df.size
            * 100
        )
    )

    st.metric(
        "Completeness",
        f"{completeness:.2f}%"
    )


# =========================================================
# 3. EXPLORE DATA
# =========================================================

elif page == "Explore Data":

    st.header("Explore Food Protein Data")

    selected_protein = st.selectbox(
        "Select Protein Source",
        [
            "All"
        ]
        + sorted(
            df["protein_source"]
            .dropna()
            .unique()
            .tolist()
        ),
    )

    if selected_protein == "All":
        filtered_df = df.copy()

    else:
        filtered_df = df[
            df["protein_source"]
            == selected_protein
        ]

    st.write(
        f"Showing {len(filtered_df)} records."
    )

    st.subheader(
        "Solubility vs pH"
    )

    fig1 = px.scatter(
        filtered_df,
        x="ph",
        y="solubility_pct",
        color="protein_source",
        hover_data=[
            "processing_method",
            "extraction_method",
            "temperature_c",
        ],
        title="Solubility and pH",
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
    )

    st.subheader(
        "Gel Strength vs Temperature"
    )

    fig2 = px.scatter(
        filtered_df,
        x="temperature_c",
        y="gel_strength_g",
        color="protein_source",
        hover_data=[
            "processing_method",
            "ph",
            "protein_concentration_pct",
        ],
        title="Gel Strength and Temperature",
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
    )

    st.subheader(
        "Average Functionality by Protein"
    )

    average_functionality = (
        filtered_df
        .groupby("protein_source")[
            [
                "solubility_pct",
                "emulsification_index",
                "foaming_capacity_pct",
                "gel_strength_g",
            ]
        ]
        .mean()
        .reset_index()
    )

    st.dataframe(
        average_functionality.round(2),
        use_container_width=True,
    )

    st.subheader(
        "Standardized Dataset"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
    )


# =========================================================
# 4. PREDICTION
# =========================================================

elif page == "Prediction":

    st.header(
        "Food Protein Solubility Prediction"
    )

    st.write(
        "Enter protein and processing conditions "
        "to generate a demonstration prediction."
    )

    col1, col2 = st.columns(2)

    with col1:

        protein_source = st.selectbox(
            "Protein Source",
            sorted(
                df["protein_source"]
                .dropna()
                .unique()
                .tolist()
            ),
        )

        protein_category = st.selectbox(
            "Protein Category",
            sorted(
                df["protein_category"]
                .dropna()
                .unique()
                .tolist()
            ),
        )

        processing_method = st.selectbox(
            "Processing Method",
            sorted(
                df["processing_method"]
                .dropna()
                .unique()
                .tolist()
            ),
        )

        extraction_method = st.selectbox(
            "Extraction Method",
            sorted(
                df["extraction_method"]
                .dropna()
                .unique()
                .tolist()
            ),
        )

    with col2:

        pH = st.slider(
            "pH",
            min_value=4.5,
            max_value=9.0,
            value=7.0,
            step=0.1,
        )

        temperature_c = st.slider(
            "Temperature (°C)",
            min_value=20.0,
            max_value=90.0,
            value=50.0,
            step=1.0,
        )

        protein_concentration_pct = st.slider(
            "Protein Concentration (%)",
            min_value=2.0,
            max_value=10.0,
            value=5.0,
            step=0.1,
        )

    input_data = pd.DataFrame({
        "protein_source": [protein_source],
        "protein_category": [protein_category],
        "ph": [pH],
        "temperature_c": [temperature_c],
        "protein_concentration_pct": [
            protein_concentration_pct
        ],
        "processing_method": [processing_method],
        "extraction_method": [extraction_method],
    })

    if st.button(
        "Predict Solubility",
        type="primary",
    ):

        prediction = model.predict(
            input_data
        )[0]

        st.success(
            f"Predicted solubility: "
            f"{prediction:.2f}%"
        )

        st.caption(
            "This is a model demonstration using "
            "synthetic data and should not be interpreted "
            "as an experimentally validated prediction."
        )


# =========================================================
# 5. MODEL EVALUATION
# =========================================================

elif page == "Model Evaluation":

    st.header(
        "Machine Learning Model Evaluation"
    )

    st.write(
        "The prototype uses a Random Forest Regression "
        "model to demonstrate basic functionality prediction."
    )

    metric_dict = dict(
        zip(
            metrics["metric"],
            metrics["value"],
        )
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "MAE",
        f"{metric_dict.get('MAE', 0):.3f}"
    )

    col2.metric(
        "RMSE",
        f"{metric_dict.get('RMSE', 0):.3f}"
    )

    col3.metric(
        "R²",
        f"{metric_dict.get('R2', 0):.3f}"
    )

    st.subheader("What do these metrics mean?")

    st.markdown(
        """
        **MAE — Mean Absolute Error**

        Represents the average absolute difference between
        predicted and observed solubility values.

        **RMSE — Root Mean Squared Error**

        Gives more weight to larger prediction errors.

        **R² — Coefficient of Determination**

        Indicates how much of the variation in the target
        variable is explained by the model on the test data.
        """
    )

    st.subheader(
        "Model Information"
    )

    st.write(
        "Model: Random Forest Regressor"
    )

    st.write(
        "Train/Test Split: 80% / 20%"
    )

    st.write(
        "Random State: 42"
    )

    st.subheader(
        "Potential Next Steps"
    )

    st.markdown(
        """
        - Replace synthetic data with carefully curated
          literature-derived or experimental data.
        - Standardize measurement units and terminology.
        - Preserve detailed experimental conditions.
        - Compare multiple machine-learning approaches.
        - Add uncertainty estimation.
        - Validate predictions using independent experimental data.
        """
    )

    st.warning(
        "Because the current dataset is synthetic, model "
        "performance should not be interpreted as evidence "
        "of real-world predictive accuracy."
    )