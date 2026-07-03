import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, KFold, cross_validate, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def run_pipeline():
    print("=== Step 1: Loading Data and Preprocessing ===")
    california = fetch_california_housing(as_frame=True)
    df = california.frame.copy()
    
    # Capping extreme outliers in AveRooms, AveOccup, AveBedrms, and Population
    df_clean = df[
        (df["AveRooms"] < 15) & 
        (df["AveOccup"] < 6) & 
        (df["AveBedrms"] < 3) & 
        (df["Population"] < 10000)
    ].copy()
    
    # Feature Engineering
    df_clean["RoomsPerHousehold"] = df_clean["AveRooms"] / df_clean["AveOccup"]
    df_clean["BedroomsPerRoom"] = df_clean["AveBedrms"] / df_clean["AveRooms"]
    df_clean["PopPerHousehold"] = df_clean["Population"] / df_clean["AveOccup"]
    
    X = df_clean.drop(columns=["MedHouseVal"])
    y = df_clean["MedHouseVal"]
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Inject 1% missing data to simulate handling of missingness (edge case)
    np.random.seed(42)
    nan_mask = np.random.rand(*X_train.shape) < 0.01
    X_train_nan = X_train.copy()
    X_train_nan[nan_mask] = np.nan
    
    print(f"Data split completed. Injected {np.isnan(X_train_nan).sum().sum()} NaNs in train set.")
    
    # Setup leakage-free pipeline components
    preprocessor = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    baseline_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', Ridge(alpha=1.0))
    ])
    
    print("\n=== Step 2: Running Cross-Validation on Baseline ===")
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_results = cross_validate(
        baseline_pipeline, X_train_nan, y_train,
        cv=cv,
        scoring=['neg_root_mean_squared_error', 'r2']
    )
    cv_rmse_base = -cv_results['test_neg_root_mean_squared_error'].mean()
    cv_r2_base = cv_results['test_r2'].mean()
    print(f"Baseline Ridge CV RMSE: {cv_rmse_base:.4f} | CV R2: {cv_r2_base:.4f}")
    
    print("\n=== Step 3: Hyperparameter Tuning for Ensemble (Random Forest) ===")
    tuned_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(random_state=42))
    ])
    
    param_distributions = {
        'regressor__n_estimators': [50, 100, 150],
        'regressor__max_depth': [10, 15, 20, None],
        'regressor__min_samples_split': [2, 5, 10],
        'regressor__max_features': ['sqrt', 'log2', None]
    }
    
    search = RandomizedSearchCV(
        tuned_pipeline,
        param_distributions=param_distributions,
        n_iter=5,
        cv=cv,
        scoring='neg_root_mean_squared_error',
        random_state=42,
        n_jobs=-1
    )
    search.fit(X_train_nan, y_train)
    best_pipeline = search.best_estimator_
    cv_rmse_rf = -search.best_score_
    print(f"Best Tuned RF CV RMSE: {cv_rmse_rf:.4f}")
    print("Best params:", search.best_params_)
    
    print("\n=== Step 4: Final Hold-Out Evaluation ===")
    # Fit baseline
    baseline_pipeline.fit(X_train_nan, y_train)
    y_pred_base = baseline_pipeline.predict(X_test)
    test_rmse_base = np.sqrt(mean_squared_error(y_test, y_pred_base))
    test_r2_base = r2_score(y_test, y_pred_base)
    
    # Fit best RF model
    y_pred_rf = best_pipeline.predict(X_test)
    test_rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    test_r2_rf = r2_score(y_test, y_pred_rf)
    
    print(f"Test Set - Baseline Ridge RMSE: {test_rmse_base:.4f} | R2: {test_r2_base:.4f}")
    print(f"Test Set - Tuned RF RMSE:       {test_rmse_rf:.4f} | R2: {test_r2_rf:.4f}")
    
    # Ensure projects output directory exists
    output_dir = os.path.join(os.path.dirname(__file__), "projects", "ml-prediction")
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n=== Step 5: Exporting Metrics Table and Plots ===")
    # Generate and save residual plots
    residuals = y_test - y_pred_rf
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    
    sns.set_theme(style="whitegrid")
    sns.scatterplot(x=y_pred_rf, y=residuals, ax=ax[0], alpha=0.3, color="teal")
    ax[0].axhline(y=0, color='r', linestyle='--')
    ax[0].set_title("Residuals vs Predicted (Tuned RF)", fontsize=14, pad=10)
    ax[0].set_xlabel("Predicted Housing Value ($100k)", fontsize=12)
    ax[0].set_ylabel("Residuals", fontsize=12)
    
    sns.histplot(residuals, kde=True, ax=ax[1], color="teal")
    ax[1].set_title("Residuals Distribution (Tuned RF)", fontsize=14, pad=10)
    ax[1].set_xlabel("Residual value", fontsize=12)
    
    plt.tight_layout()
    plot_path = os.path.join(output_dir, "residuals.png")
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"Saved residual plots to {plot_path}")
    
    # Save the best model to a pickle file
    import pickle
    model_path = os.path.join(output_dir, "best_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(best_pipeline, f)
    print(f"Saved best model pickle to {model_path}")
    
    # Generate and save feature importances plot
    rf_model = best_pipeline.named_steps['regressor']
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    feature_names = X.columns
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importances[indices], y=feature_names[indices], color="teal")
    plt.title("Feature Importances - Tuned Random Forest Regressor", fontsize=14, pad=15)
    plt.xlabel("Relative Importance Score", fontsize=12)
    plt.ylabel("Features", fontsize=12)
    plt.tight_layout()
    
    fi_plot_path = os.path.join(output_dir, "feature_importance.png")
    plt.savefig(fi_plot_path, dpi=150)
    plt.close()
    print(f"Saved feature importance plot to {fi_plot_path}")
    
    # Create the markdown metrics table
    metrics_content = f"""# Model Performance Metrics Table

This table compares the performance of the Baseline Ridge Regression model and the Tuned Random Forest Regressor on the California Housing dataset.

| Model / Estimator | CV Mean RMSE | CV Mean R² | Test Set RMSE | Test Set R² |
| :--- | :---: | :---: | :---: | :---: |
| **Baseline Ridge Regression** | {cv_rmse_base:.4f} | {cv_r2_base:.4f} | {test_rmse_base:.4f} | {test_r2_base:.4f} |
| **Tuned Random Forest Regressor** | {cv_rmse_rf:.4f} | - | {test_rmse_rf:.4f} | {test_r2_rf:.4f} |

### Observations:
* The **Tuned Random Forest Regressor** achieves a significantly lower Root Mean Squared Error (RMSE) on the test set ({test_rmse_rf:.4f}) compared to the Ridge model ({test_rmse_base:.4f}).
* The tuned model accounts for roughly **{test_r2_rf * 100:.1f}%** of the variance in California housing prices ($R^2$ of {test_r2_rf:.4f}), which is a large improvement over the baseline ({test_r2_base * 100:.1f}%).
"""
    metrics_path = os.path.join(output_dir, "metrics_table.md")
    with open(metrics_path, "w", encoding="utf-8") as f:
        f.write(metrics_content)
    print(f"Saved metrics table to {metrics_path}")
    
    print("\nPipeline execution finished successfully!")

if __name__ == "__main__":
    run_pipeline()
