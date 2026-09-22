# FoodProt-Lite

## A Small Educational Prototype for Food Protein Functionality Data

FoodProt-Lite is an independent educational prototype inspired by the data-standardization and predictive-modeling challenges involved in food protein research.

The project explores a simple question:

> How can fragmented food-protein functionality information be organized into a structured dataset and then used for exploratory analysis and basic machine learning?

## Project Features

* Synthetic food-protein dataset with 250+ records
* Data cleaning and standardization pipeline
* Duplicate and missing-value handling
* Data-quality assessment
* Exploratory data analysis
* Food protein functionality visualization
* Random Forest regression model
* Solubility prediction
* Model evaluation using MAE, RMSE, and R²
* Interactive Streamlit dashboard

## Workflow

```text
Synthetic Food-Protein Data
            ↓
     Data Cleaning
            ↓
   Standardization
            ↓
    Data Quality Check
            ↓
 Exploratory Data Analysis
            ↓
     Machine Learning
            ↓
  Solubility Prediction
```

## Why I Built This Prototype

While learning about food protein functionality research, I became interested in the challenge of organizing information from different experiments and studies into a structured and comparable format.

This small prototype was created to explore that idea from a computational perspective.

The focus is not on recreating an existing research database, but on understanding how data organization, quality assessment, exploratory analysis, and machine learning can work together in food science research.

## Data

The current dataset is **synthetic** and was created specifically for educational and demonstration purposes.

The dataset contains information such as:

* Protein source
* Protein category
* pH
* Temperature
* Protein concentration
* Processing method
* Extraction method
* Measurement method
* Solubility
* Emulsification
* Foaming
* Gel strength

The synthetic dataset allows the complete workflow to be demonstrated without presenting simulated values as experimental scientific results.

## Data Processing

The data-processing pipeline performs several basic steps:

1. Standardizes column names
2. Removes duplicate records
3. Checks basic numerical validity
4. Identifies missing values
5. Fills missing numerical values using median values
6. Handles missing categorical values
7. Generates a data-quality report
8. Saves the standardized dataset for analysis

## Machine Learning

A **Random Forest Regression** model is used as a simple demonstration of predictive modeling.

### Target Variable

`solubility_pct`

### Input Features

* Protein source
* Protein category
* pH
* Temperature
* Protein concentration
* Processing method
* Extraction method

Categorical variables are encoded using a preprocessing pipeline, while numerical variables are passed directly to the model.

The dataset is divided into training and testing subsets using an 80/20 split.

## Model Evaluation

The model is evaluated using:

* Mean Absolute Error (MAE)
* Root Mean Squared Error (RMSE)
* R² score

These metrics are included to demonstrate how a basic predictive model can be evaluated rather than simply reporting a single accuracy value.

## Streamlit Dashboard

The project includes an interactive Streamlit application with several sections:

### 1. Overview

Provides a summary of the dataset and the complete workflow.

### 2. Data Quality

Shows:

* Number of records
* Missing values
* Duplicate records
* Data completeness
* Data-quality report

### 3. Explore Data

Allows users to:

* Filter protein sources
* Explore relationships between variables
* View functionality measurements
* Compare average functionality across protein sources

### 4. Prediction

Allows users to enter food-protein processing conditions and generate a demonstration solubility prediction using the trained model.

### 5. Model Evaluation

Displays the model's MAE, RMSE, and R² metrics.

## Scientific Limitations

This prototype has important limitations.

The dataset is **synthetic**, so the model results should not be interpreted as experimentally validated scientific findings.

Real food-protein research would require carefully collected experimental or literature-derived data, standardized measurement units, detailed experimental conditions, appropriate validation, and independent testing.

The current prototype is therefore intended only as an educational demonstration of a possible computational workflow.

## Future Extensions

A future version could incorporate:

* Literature-derived real food-protein data
* Experimental methods and measurement units
* Standardized terminology across studies
* Additional protein functionality measurements
* Protein sequence or structural features
* Molecular or structural descriptors
* More machine-learning models
* Model uncertainty and interpretability
* Independent validation using experimental datasets

## Technologies

* Python
* Pandas
* NumPy
* Scikit-learn
* Plotly
* Streamlit
* Joblib

## Project Structure

```text
FoodProt-Lite/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── food_protein_raw.csv
│   └── processed/
│       └── food_protein_standardized.csv
│
├── models/
│   └── functionality_model.pkl
│
├── reports/
│   ├── data_quality_report.csv
│   └── model_metrics.csv
│
└── src/
    ├── __init__.py
    ├── generate_data.py
    ├── clean_data.py
    └── train_model.py
```

## Installation

Clone the repository and install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the Project

First generate the synthetic dataset:

```bash
python src/generate_data.py
```

Then clean and standardize the dataset:

```bash
python src/clean_data.py
```

Train the machine-learning model:

```bash
python src/train_model.py
```

Finally, launch the Streamlit application:

```bash
streamlit run app.py
```

## Author

**Aqsa Kanwal**

BS Food Science & Technology

Interests:

* Food Science
* Food Quality
* Functional Foods
* Food Product Development
* Alternative Proteins
* AI/ML Applications in Food Science
