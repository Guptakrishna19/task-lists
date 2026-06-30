# Executive Summary: E-Commerce Cohort Retention & Lifetime Value (LTV) Analysis

## 1. Objective & Business Context
This analysis evaluates customer engagement and spending behaviors for 150 customers who signed up between January and March 2026. We track each customer's transaction activity for 6 months post-signup (Month 0 through Month 5) to measure lifecycle retention decay and cumulative Lifetime Value (LTV) growth. The goal is to identify churn patterns and formulate strategic recommendations to optimize customer retention and acquisition spending.

---

## 2. Methodology & Data Quality Checks
To ensure data integrity and avoid skewing high-level financial metrics, we implemented pre-processing steps in Pandas to resolve four core edge cases:
* **Duplicate Rows:** Removed duplicate transaction rows based on unique `order_id` to prevent double-counting revenue.
* **Missing Values:** Imputed missing acquisition segments with `'Unknown'` and dropped order records with null transaction values.
* **Negative Values:** Filtered out negative transaction amounts resulting from database sync errors.
* **Malformed Dates:** Safely parsed datetime fields using coercion (`errors='coerce'`) and dropped unparseable records to ensure accurate cohort index calculations.

Once cleaned, datasets were loaded into an SQLite database and joined via SQL to aggregate customer-level orders.

---

## 3. Core Insights
1. **Retention Decay Curves:**
   * Across all monthly cohorts, customer retention starts at **Month 0 (100.0%)** as the baseline purchase month.
   * There is a steep drop in **Month 1 (ranging from ~29% to 37%)**, highlighting a strong cohort of one-time buyers who do not return within 30 days of their initial purchase.
   * By **Month 5**, cohort retention stabilizes between **10% and 15%** for the mature cohorts, representing our loyal repeat buyers.
2. **LTV Growth & Cumulative Spend:**
   * Cumulative customer spend (LTV) increases steadily over time, but the growth rate slows as customer retention decays.
   * On average, a customer generates **~$56 to $78** in revenue during Month 0. By Month 5, the cumulative LTV ranges between **$171 and $198** per customer.
   * Cohorts that maintain slightly higher repeat purchase rates in Months 1 and 2 show a visible lift in overall cumulative LTV by Month 5.

---

## 4. Actionable Strategic Recommendations
* **Implement a Month 1 Re-Engagement Flow:** Because the largest drop-off in customer retention occurs in the first 30 days (Month 1), marketing should deploy automated email sequences, SMS alerts, or personalized product recommendations at day 15 and day 25 post-signup. Offering a \"second purchase discount\" can incentivize repeat visits.
* **Focus on Retention over Acquisition:** Since customers who are retained through Month 5 generate nearly 3x the revenue of a one-time buyer (raising LTV from $55 to over $170), shifting 15% of the marketing budget from customer acquisition to retention loyalty campaigns (such as a tiered rewards program) will improve profitability.
* **Acquisition Channel Optimization:** Segment-based analysis shows variations in value. We recommend tracking LTV by acquisition source (Organic vs. Paid Ads) to reallocate budget toward channels bringing in cohorts with higher retention curves.
