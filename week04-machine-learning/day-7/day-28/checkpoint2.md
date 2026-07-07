# Checkpoint 2

## Objective
Audit for leakage/overfitting and productionize training by moving it to `train.py`.

## Data Leakage Audit
- **Issue Checked:** Applying data scaling to the entire dataset before splitting it into train and validation sets is a common cause of data leakage.
- **Fix:** In `train.py`, `StandardScaler` is explicitly fitted **only** on `X_train` via a Scikit-Learn `Pipeline`, and then used to transform the validation/test data. This ensures no information from the test set leaks into the training process.

## Overfitting Detection
- **Check:** Compared training R2/RMSE vs. validation/test R2/RMSE.
- **Result:**
  - An unconstrained model memorized the training data resulting in an enormous gap between training and validation scores.
  - Used `RandomForestRegressor(max_depth=15, min_samples_split=5)` to prevent the trees from growing too deep and memorizing the training data.
  - The gap between training accuracy and validation accuracy is monitored in `train.py`. If it exceeds 10%, an overfitting warning is printed.

## Deliverables
- `train.py` created and successfully handles data loading, pipeline execution, metrics generation, and handles edge cases (like empty datasets or NaN targets).
- `best_model.pkl` and `metrics.md` are automatically saved.

## Reflection
- **What was difficult:** Finding the right hyperparameter constraints to prevent the Random Forest model from memorizing the data.
- **What I improved:** Transitioned from fragile Jupyter notebooks to a robust, reproducible `train.py` script. Enforced strict data leakage prevention using Scikit-Learn Pipelines.
- **What remains:** Integrating an experiment tracking system (like MLflow) and wrapping the model in a REST API for real-time predictions.