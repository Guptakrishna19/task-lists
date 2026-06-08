# Debugging Documentation — Day 7

This document describes the 3 bugs intentionally introduced in `debugging_exercises.py` and how they were debugged and fixed.

## Bug 1: Off-by-One Error in `average_first_n()`

### The Bug
```python
# BUGGY VERSION:
for index in range(n + 1):  # ❌ This iterates one too many times
    total += numbers[index]  # Can raise IndexError
```

### Problem
- `range(n + 1)` generates values from 0 to n (inclusive), which is one extra iteration
- When n = 3 and the list has only 3 elements (indices 0, 1, 2), trying to access index 3 raises `IndexError`
- Example: `average_first_n([10, 20, 30, 40], 3)` would fail trying to access index 3

### How It Was Fixed
```python
# FIXED VERSION:
for index in range(n):  # ✅ Correct: 0 to n-1
    total += numbers[index]
```

### Debugging Method
- Used `breakpoint()` to inspect the loop and see the IndexError
- Checked the `range()` output: `list(range(3))` = [0, 1, 2] vs `list(range(3 + 1))` = [0, 1, 2, 3]
- Removed the `+ 1` from the range

---

## Bug 2: KeyError in `get_user_email()`

### The Bug
```python
# BUGGY VERSION:
return user["email"]  # ❌ Raises KeyError if "email" key doesn't exist
```

### Problem
- Dictionary access with `user["email"]` throws `KeyError` when the key is missing
- Example: `get_user_email({"name": "Kavya"})` crashes because "email" key is not present
- No graceful fallback for missing data

### How It Was Fixed
```python
# FIXED VERSION:
return user.get("email", "No email found")  # ✅ Safe dictionary access with default
```

### Debugging Method
- Used `breakpoint()` to inspect the user dictionary
- Checked what keys were actually present: `user.keys()`
- Switched to `.get()` method which returns a default value if key is missing
- Provided a meaningful fallback message

---

## Bug 3: TypeError in `add_bonus()`

### The Bug
```python
# BUGGY VERSION:
return score + bonus  # ❌ TypeError: can't add string + int
```

### Problem
- When `score` is passed as a string (e.g., `"85"`), Python can't add it to an integer
- Example: `add_bonus("85", 5)` fails with `TypeError: can only concatenate str (not "int") to str`
- The function needs to handle both string and numeric inputs

### How It Was Fixed
```python
# FIXED VERSION:
return int(score) + int(bonus)  # ✅ Convert both to integers first
```

### Debugging Method
- Used `breakpoint()` to check the type of `score`
- Ran `type(score)` in the debugger and saw it was `<class 'str'>`
- Converted both inputs to `int()` before addition
- Added input validation to ensure they're numeric before converting

---

## Summary of Bugs

| Bug | Type | Cause | Fix |
|-----|------|-------|-----|
| Bug 1 | IndexError (off-by-one) | Loop range too large | Remove `+ 1` from `range(n + 1)` |
| Bug 2 | KeyError (missing key) | Direct dict access | Use `.get()` with default |
| Bug 3 | TypeError (type mismatch) | String vs int | Convert inputs with `int()` |

## Key Debugging Techniques Used

1. **Breakpoints**: Use `breakpoint()` to pause execution and inspect variables
2. **Type checking**: Use `type()` to understand variable types
3. **Dictionary inspection**: Use `.keys()` and `.get()` for safe access
4. **Range verification**: Understand how `range()` works (0 to n-1, not n)

## Testing the Fixed Code

Run the fixed version:
```bash
python debugging_exercises.py
```

Expected output:
```
Exercise 1: 20.0
Exercise 2: No email found
Exercise 3: 90
```

All functions now handle edge cases gracefully without raising unhandled exceptions.

### Learning
Check data types before doing arithmetic, especially when values may come from input, files, or APIs.
