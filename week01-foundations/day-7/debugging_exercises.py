"""
Day 7 debugging exercises.

Run this file with:
    python week01-foundations/day-7/debugging_exercises.py

Each exercise includes the original bug as a comment and the fixed code below it.
To practice with pdb, uncomment a breakpoint() line and inspect the variables.
"""


def average_first_n(numbers, n):
    """Return the average of the first n numbers."""
    if n <= 0:
        raise ValueError("n must be positive.")
    if n > len(numbers):
        raise ValueError("n cannot be larger than the list length.")

    total = 0
    # Bug: range(n + 1) reads one extra item and can raise IndexError.
    # breakpoint()
    for index in range(n):
        total += numbers[index]

    return total / n


def get_user_email(user):
    """Return a user's email or a clear fallback message."""
    # Bug: user["email"] raises KeyError when the key is missing.
    # breakpoint()
    return user.get("email", "No email found")


def add_bonus(score, bonus):
    """Add a numeric bonus to a numeric score."""
    # Bug: adding "85" + 5 raises TypeError because score is a string.
    # breakpoint()
    return int(score) + int(bonus)


def run_exercises():
    print("Exercise 1:", average_first_n([10, 20, 30, 40], 3))
    print("Exercise 2:", get_user_email({"name": "Kavya"}))
    print("Exercise 3:", add_bonus("85", 5))


if __name__ == "__main__":
    run_exercises()
