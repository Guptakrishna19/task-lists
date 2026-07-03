# California Housing Price Prediction Project

This project implements an end-to-end supervised machine learning pipeline to predict California house prices based on the classic 1990 US Census data. The project contains data exploration, cleaning of outliers, robust scaling, leakage-free pipelines, cross-validation, and hyperparameter tuning using Random Forest Regressors.

## Project Structure

All files for this project are self-contained inside the `day-27/` folder:

*   **`exercise.ipynb`**: Contains step-by-step EDA, missing value injection testing, leakage-free `Pipeline` verification, 5-fold cross-validation, and `RandomizedSearchCV` hyperparameter tuning.
*   **`pipeline.py`**: A clean, reproducible, production-ready Python script automating the full execution from data load to model evaluation, saving residual plots and metrics tables.
*   **`projects/ml-prediction/`**:
    *   **`README.md`**: This summary file.
    *   **`MODEL_CARD.md`**: The AI Model Card documenting model specifications, intended use, limitations, data, and ethical considerations.
    *   **`metrics_table.md`**: A table comparing baseline Ridge regression vs. the tuned Random Forest model.
    *   **`residuals.png`**: Visual diagnostics plot of prediction errors and their distribution.
    *   **`feature_importance.png`**: Visual bar plot of relative feature importance scores.
    *   **`best_model.pkl`**: Serialized python pickle containing the final tuned pipeline.

## How to Run & Reproduce Results

To run the pipeline and regenerate the metrics table and plots:

1.  **Activate Environment**:
    ```powershell
    .\.venv\Scripts\activate
    ```
2.  **Execute Script**:
    ```powershell
    python task-lists/week04-machine-learning/day-6/day-27/pipeline.py
    ```
3.  **Inspect Outputs**:
    Check the files inside `task-lists/week04-machine-learning/day-6/day-27/projects/ml-prediction/` for updated metrics and the diagnostic plots.
