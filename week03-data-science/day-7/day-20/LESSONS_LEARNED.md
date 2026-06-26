# Lessons Learned: Revision, Debugging & Refactoring (Day 21)

This document summarizes the insights, design patterns, and engineering takeaways from refactoring exploratory data science notebooks into production-grade pipelines.

---

## 1. Difficulties and Blockers
*   **State Alignment in Dashboards:** Handling user actions in Streamlit requires strict state preservation using `st.session_state` to prevent inputs from wiping out on script reruns.
*   **Window Functions Execution Context:** SQL window functions cannot be placed directly in the `WHERE` clause; they require Common Table Expressions (CTEs) or subqueries to resolve execution orders, which was initially confusing but resolved by establishing standard CTE scaffolding.
*   **Standardizing Raw Inputs:** Cleansing string values with stripping and case conversion handles missing categories, but mapping functions had to be adapted to handle unexpected whitespace and capitalization cases.

---

## 2. Refactoring & Code Quality Improvements
*   **Linear Execution:** Moving code from arbitrary notebook cells to modular modules like [cleaning.py](file:///c:/Users/Kavya/Desktop/task-list/task-lists/week03-data-science/day-7/day-20/src/cleaning.py) and [features.py](file:///c:/Users/Kavya/Desktop/task-list/task-lists/week03-data-science/day-7/day-20/src/features.py) enforces a deterministic, testable data pipeline.
*   **Safety Guards and Exception Checking:** All operations, including division and datatype parsing, now have checks for empty series/DataFrames and null divisions.
*   **Readability:** Nested subqueries are now completely replaced with CTEs, which divides queries into self-documenting modules.

---

## 3. What Remains (Future Steps)
*   **Unit Tests:** Implementing structured tests with `pytest` for `src/cleaning.py` and `src/features.py` to assert expected outcomes for edge cases automatically.
*   **CI/CD Pipeline integration:** Adding automated formatting with `black` and linting with `flake8` to prevent syntactical bugs before commits.
