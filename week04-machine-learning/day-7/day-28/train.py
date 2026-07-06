import os
import pickle
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

def load_and_preprocess_data():
    print("Loading California Housing dataset...")
    california = fetch_california_housing(as_frame=True)
    df = california.frame.copy()
    
    # Capping extreme outliers (similar to Day 27)
    df_clean = df[
        (df["AveRooms"] < 15) & 
        (df["AveOccup"] < 6) & 
        (df["AveBedrms"] < 3) & 
        (df["Population"] < 10000)
    ].copy()
    
    # Edge Case 1: Drop rows where target variable is NaN
    df_clean = df_clean.dropna(subset=["MedHouseVal"])
    
    # Edge Case 2: Ensure dataset is not empty after filtering
    if df_clean.empty:
        raise ValueError("Error: The dataset is empty after outlier and NaN removal.")
    
    # Feature Engineering
    df_clean["RoomsPerHousehold"] = df_clean["AveRooms"] / df_clean["AveOccup"]
    df_clean["BedroomsPerRoom"] = df_clean["AveBedrms"] / df_clean["AveRooms"]
    df_clean["PopPerHousehold"] = df_clean["Population"] / df_clean["AveOccup"]
    
    X = df_clean.drop(columns=["MedHouseVal"])
    y = df_clean["MedHouseVal"]
    
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_and_evaluate():
    # 1. Load and split data
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    print(f"Training data shape: {X_train.shape}")
    print(f"Testing data shape: {X_test.shape}")
    
    # 2. Build leakage-free pipeline with constrained model (prevent overfitting)
    # Based on Day 27, we use max_depth=15, min_samples_split=5 for robustness
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('regressor', RandomForestRegressor(
            n_estimators=100, 
            max_depth=8, 
            min_samples_split=10,
            random_state=42
        ))
    ])
    
    # 3. Train model
    print("\nTraining the model (this may take a few moments)...")
    pipeline.fit(X_train, y_train)
    
    # 4. Predict and evaluate on both sets to check for overfitting gap
    y_train_pred = pipeline.predict(X_train)
    y_test_pred = pipeline.predict(X_test)
    
    train_r2 = r2_score(y_train, y_train_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    
    test_r2 = r2_score(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    
    print("\n--- Evaluation Metrics ---")
    print(f"Train R2: {train_r2:.4f} | Train RMSE: {train_rmse:.4f}")
    print(f"Test  R2: {test_r2:.4f} | Test  RMSE: {test_rmse:.4f}")
    
    gap = train_r2 - test_r2
    if gap > 0.10:
        print("Overfitting Warning! Train-vs-Test R2 gap is {:.4f} (>10%)".format(gap))
    else:
        print("Gap is acceptable ({:.4f})".format(gap))

    # 5. Save model
    output_dir = os.path.dirname(__file__)
    model_path = os.path.join(output_dir, "best_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(pipeline, f)
    print(f"\nModel saved successfully to: {model_path}")
    
    warning_msg = f"⚠️ **Overfitting Warning!** Gap is {gap:.4f} (>10%)" if gap > 0.10 else f"✅ Gap is acceptable ({gap:.4f})"
    
    # 6. Save metrics table
    metrics_path = os.path.join(output_dir, "metrics.md")
    metrics_content = f"""# Final Model Metrics

| Split | R² Score | RMSE |
| :--- | :---: | :---: |
| **Train** | {train_r2:.4f} | {train_rmse:.4f} |
| **Test (Hold-out)** | {test_r2:.4f} | {test_rmse:.4f} |

**Overfitting Check:** Train-vs-Test R² gap is {gap:.4f}. 
{warning_msg}
"""
    with open(metrics_path, "w", encoding="utf-8") as f:
        f.write(metrics_content)
    print(f"Metrics saved successfully to: {metrics_path}")

if __name__ == "__main__":
    train_and_evaluate()
