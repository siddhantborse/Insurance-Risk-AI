# Surprise Bill Risk Predictor - Notebook Pipeline

## Recommended order
1. `01_data_understanding_and_baseline_cleaning.ipynb`
2. `02_feature_engineering_and_proxy_labels.ipynb`
3. `03_model_training_and_evaluation.ipynb`
4. `04_scoring_new_cases_and_presentation_dashboard_data.ipynb`

## Input
Place your cleaned CSV at:
`data/cleaned_cms.csv`

## Core idea
This project uses public CMS-style financial/provider data to estimate surprise-billing exposure with:
- feature engineering
- proxy target creation
- classification
- regression
- source-of-risk prediction

## Designed for a normal machine
The notebooks use:
- pandas
- scikit-learn
- matplotlib
- joblib

No GPU is required.

## Presentation storyline
- Notebook 1: prove data quality and coverage
- Notebook 2: explain your financial and service-risk features
- Notebook 3: show machine learning results
- Notebook 4: demo scoring, dashboard tables, and scenario simulation
