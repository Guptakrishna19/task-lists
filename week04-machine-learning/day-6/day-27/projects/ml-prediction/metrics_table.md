# Model Performance Metrics Table

This table compares the performance of the Baseline Ridge Regression model and the Tuned Random Forest Regressor on the California Housing dataset.

| Model / Estimator | CV Mean RMSE | CV Mean R² | Test Set RMSE | Test Set R² |
| :--- | :---: | :---: | :---: | :---: |
| **Baseline Ridge Regression** | 0.6696 | 0.6630 | 0.6632 | 0.6719 |
| **Tuned Random Forest Regressor** | 0.5195 | - | 0.5038 | 0.8106 |

### Observations:
* The **Tuned Random Forest Regressor** achieves a significantly lower Root Mean Squared Error (RMSE) on the test set (0.5038) compared to the Ridge model (0.6632).
* The tuned model accounts for roughly **81.1%** of the variance in California housing prices ($R^2$ of 0.8106), which is a large improvement over the baseline (67.2%).
