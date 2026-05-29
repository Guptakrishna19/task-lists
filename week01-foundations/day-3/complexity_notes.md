# Day 3 — Complexity Notes
## Data Structures & Big-O Annotations

---

## Quick Reference: Big-O Cheat Sheet

| Notation | Name | Example |
|---|---|---|
| O(1) | Constant | Dict/set lookup, list index access |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Single loop through a list |
| O(n log n) | Linearithmic | Python's built-in sort (Timsort) |
| O(n²) | Quadratic | Nested loop over the same list |

**Rule of thumb:** if you can replace a nested loop with a dict/set lookup, you drop from O(n²) → O(n). That's the biggest win in this session.

---

## Data Structure Operations

| Operation | Structure | Time | Space |
|---|---|---|---|
| Lookup by key | dict / set | O(1) avg | O(n) |
| Lookup by index | list | O(1) | O(1) |
| Search (unsorted) | list | O(n) | O(1) |
| Insert | dict / set | O(1) avg | O(n) |
| Sort | list | O(n log n) | O(1)–O(n) |
| Nested loop | list | O(n²) | O(1) |

---

## Problem-by-Problem Annotations

---

### Problem 1 — Remove duplicates from a list
**Approach:** Cast list → set → list  
**Time:** O(n) — iterates through all n elements once to build the set  
**Space:** O(n) — the set stores up to n unique elements  
**Note:** Does NOT preserve original order. Use Problem 2 if order matters.

---

### Problem 2 — Dedupe while preserving order
**Approach:** Loop + a `seen` set to track first appearances  
**Time:** O(n) — one pass through the list; each `in seen` check is O(1)  
**Space:** O(n) — the `seen` set grows with unique elements  
**Note:** Using a list instead of a set for `seen` would make each check O(n), turning the whole thing O(n²). The set is the key.

---

### Problem 3 — Count word frequencies
**Approach:** Single loop with `dict.get(word, 0) + 1`  
**Time:** O(n) — one pass, O(1) dict operations each step  
**Space:** O(k) — where k = number of unique words (k ≤ n)  
**Note:** `Counter` from `collections` does the same thing with less code, same complexity.

---

### Problem 4 — Top-k most frequent elements
**Approach:** `Counter` + `.most_common(k)`  
**Time:** O(n log n) — counting is O(n), sorting the frequency dict is O(n log n)  
**Space:** O(n) — frequency dict holds all unique elements  
**Note:** For very large n with small k, a heap solution can do O(n log k), but `.most_common()` is fine for most cases.

---

### Problem 5 — Two-sum (return indices)
**Approach:** Single pass; store each number's index in a dict, check for complement  
**Time:** O(n) — one loop, O(1) lookup each step  
**Space:** O(n) — dict stores up to n entries  
**Note:** Naive nested-loop approach is O(n²). The dict eliminates the inner loop entirely. This is the most important pattern from Day 3.

---

### Problem 6 — Two-sum (return values)
**Approach:** Same as Problem 5 but using a `set` (no index needed)  
**Time:** O(n)  
**Space:** O(n)  
**Note:** Use a set (not dict) when you only need to know if a value exists, not where it is. Slightly leaner.

---

### Problem 7 — Group strings by first letter
**Approach:** `defaultdict(list)` — use first char as key, append to list  
**Time:** O(n) — one pass, O(1) dict operations  
**Space:** O(n) — all strings stored across the groups  
**Note:** `defaultdict(list)` auto-creates an empty list for new keys, avoiding a manual `if key not in d` check every iteration.

---

### Problem 8 — Group anagrams together
**Approach:** Sort each word's characters → use as dict key  
**Time:** O(n · m log m) — n words, each sorted in O(m log m) where m = word length  
**Space:** O(n) — all words stored in groups  
**Note:** The sorted-characters trick is the key insight. Two anagrams always produce the same sorted string, making them hash to the same bucket.

---

### Problem 9 — Sort list of dicts by a key
**Approach:** `sorted()` with `key=lambda r: r["field"]`  
**Time:** O(n log n) — Python's Timsort  
**Space:** O(n) — `sorted()` returns a new list; `.sort()` is O(1) space (in-place)  
**Note:** Python's sort is *stable* — equal elements keep their original relative order. Safe to use for tiebreaking.

---

### Problem 10 — Sort by multiple keys
**Approach:** Return a tuple from the key function: `key=lambda r: (r["dept"], -r["salary"])`  
**Time:** O(n log n)  
**Space:** O(n)  
**Note:** Python compares tuples left-to-right. The `-` negates a numeric field to sort it descending while the primary key stays ascending. For strings, you need two separate `sorted()` calls with `reverse` flags.

---

## Key Takeaways

- **Set for membership checks** — if you're asking "have I seen this before?", use a set. O(1) vs O(n) for lists.
- **Dict for mapping** — any time you need to associate a value with a key (counts, complements, groups), reach for a dict.
- **One pass is usually enough** — most O(n²) solutions can be rewritten as a single loop + a dict.
- **`defaultdict`** saves boilerplate when building dicts of lists or dicts of counts.
- **`sorted(key=...)`** is your friend — Timsort is fast and stable, no need to implement your own.

---

## Self-Review

- What was difficult:
- What improved:
- What remains: