# Week 01: Foundations

A comprehensive introduction to Python fundamentals covering data structures, file I/O, debugging, and best practices.

## Overview

This week contains daily exercises and tasks that build core programming skills:

- **Day 1**: Python basics and syntax
- **Day 2**: Functions and code organization  
- **Day 3**: Complexity analysis and algorithm design
- **Day 4**: Testing and modules (banking system example)
- **Day 5**: File I/O and working with JSON/CSV data
- **Day 6**: Data manipulation and analysis
- **Day 7**: Debugging techniques and code refactoring

## Project Structure

```
week01-foundations/
├── day-2/                    # Functions basics
├── day-3/                    # Complexity analysis
├── day-4/                    # Testing & modules
│   └── src/banking.py        # Banking module
│   └── tests/test_banking.py # Unit tests
├── day-5/                    # File I/O
│   └── src/fetch_data.py     # Data fetching example
├── day-6/                    # Data analysis
├── day-7/                    # Debugging & refactoring
│   ├── refactored_module.py  # Cleaned-up utilities module
│   ├── debugging_exercises.py# Bug fixing examples with fixes
│   ├── week01_day7.ipynb     # Exercise and task notebook
│   ├── DEBUGGING.md          # Detailed bug documentation
│   └── SELF-REVIEW.md        # Learning outcomes & reflection
├── notebooks/                # Jupyter notebooks for each day
└── requirements.txt          # Python dependencies
```

## Key Concepts

### Functions & Modularity
- Writing clear, reusable functions
- Using docstrings for documentation
- Following naming conventions

### Testing
- Unit testing with pytest
- Test-driven development basics
- Handling edge cases

### File I/O
- Reading and writing files (text, CSV, JSON)
- Working with external APIs
- Error handling for file operations

### Debugging
- Using Python debugger (pdb)
- Identifying common bugs (off-by-one, KeyError, TypeError)
- Writing reproducible test cases

## How to Use

### Run Python Scripts
```bash
# Test the refactored module
python week01-foundations/day-7/refactored_module.py

# Run debugging exercises
python week01-foundations/day-7/debugging_exercises.py
```

### Run Tests
```bash
# Unit tests for banking module (Day 4)
cd week01-foundations/day-4
python -m pytest tests/test_banking.py -v
```

### View Notebooks & Self-Review
```bash
# Open Jupyter to view notebooks
jupyter notebook week01-foundations/notebooks/days/

# Read learning reflections
cat week01-foundations/day-7/SELF-REVIEW.md
cat week01-foundations/day-7/DEBUGGING.md
```

## Requirements

See [requirements.txt](requirements.txt) for dependencies:
- Python 3.8+
- pytest (for testing)
- jupyter (for notebooks)

## Learning Outcomes

By the end of this week, you should be able to:

✅ Write clean, documented Python functions  
✅ Organize code into modules  
✅ Write unit tests for your code  
✅ Read and write data files (CSV, JSON)  
✅ Debug code effectively using pdb  
✅ Refactor messy code following best practices  

## Key Takeaways

- **Code clarity matters**: Good naming, docstrings, and comments save time.
- **Test everything**: Edge cases and error handling are crucial.
- **Debugging is a skill**: Learn pdb to find bugs faster.
- **Refactoring improves code**: Regular cleanup prevents technical debt.

## Week 01 Completion Summary

### ✅ Completed Deliverables

**Day 7: Revision + Debugging**
- ✅ Refactored messy utility functions from Day 2 with clear naming and docstrings
- ✅ Fixed 3 common bugs (off-by-one, KeyError, TypeError) with detailed explanations
- ✅ Created comprehensive project README
- ✅ Wrote DEBUGGING.md documenting bug patterns and fixes
- ✅ Completed SELF-REVIEW.md with learnings and key takeaways

### 📚 Resources

- **Debugging reference**: See [DEBUGGING.md](day-7/DEBUGGING.md) for bug patterns and pdb techniques
- **Refactored code**: See [refactored_module.py](day-7/refactored_module.py) for clean code examples
- **Learning reflection**: See [SELF-REVIEW.md](day-7/SELF-REVIEW.md) for outcomes and blockers

### 📝 Notes

All exercises are self-contained and can be run independently. Each day builds on previous concepts but focuses on specific topics.

For detailed notes on specific days, see the reflection markdown files in each day's folder.
