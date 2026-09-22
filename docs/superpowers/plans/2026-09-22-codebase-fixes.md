# Codebase Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix 4 code quality issues identified during docs-mcp verification of the Rutos-tranScripter project.

**Architecture:** All changes are mechanical fixes across 4 files. No new abstractions, no interface changes. Each task is independent and produces a testable deliverable.

**Tech Stack:** Python 3.13, NumPy, NLTK, Ruff, mypy

**Spec:** `docs/superpowers/specs/2026-09-22-codebase-fixes-design.md`

## Global Constraints

- `requires-python = ">=3.13"` (exact from pyproject.toml)
- No new dependencies
- `make lint && make typecheck && make test && make e2e` must pass after each task
- Single commit at end: `Fix: improve code quality per docs-mcp verification`

---

### Task 1: Add SIM Ruff Rule Group

**Files:**
- Modify: `pyproject.toml` (lines 28-40)
- No new tests (config change, tested by lint pass)

**Interfaces:**
- Consumes: current pyproject.toml `[tool.ruff.lint]` section
- Produces: updated select list with `"SIM"` added

- [ ] **Step 1: Read current pyproject.toml**

Read `pyproject.toml` lines 28-40 to confirm current select list.

- [ ] **Step 2: Add "SIM" to ruff select**

In `[tool.ruff.lint]` section, add `"SIM",` to the `select` list:

```toml
[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
]
```

- [ ] **Step 3: Run ruff check to see what SIM catches**

Run: `ruff check .`
Expected: May surface issues in machine.py (list concat) and arithmeticEnv.py (bare Exception). These will be fixed in later tasks.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml
git commit -m "chore: add SIM ruff rule group for flake8-simplify"
```

---

### Task 2: Fix List Concatenation in Machine

**Files:**
- Modify: `JAVS_Util/machine.py` (line 28)
- No new tests

**Interfaces:**
- Consumes: existing `Machine.generatePythonCode()` signature
- Produces: same return type `list[str]`, identical behavior

- [ ] **Step 1: Read machine.py to find the line**

Open `JAVS_Util/machine.py`, find line 28 which contains:
```python
python_code = [*python_code, *python_code_sentence]
```

- [ ] **Step 2: Replace with extend()**

Replace line 28 with:
```python
python_code.extend(python_code_sentence)
```

- [ ] **Step 3: Run lint to verify fix**

Run: `ruff check JAVS_Util/machine.py`
Expected: No SIM violations on this file now.

- [ ] **Step 4: Run tests**

Run: `make test && make e2e`
Expected: All tests pass (behavior unchanged).

- [ ] **Step 5: Commit**

```bash
git add JAVS_Util/machine.py
git commit -m "refactor: use extend() instead of spread concat in Machine.generatePythonCode"
```

---

### Task 3: Replace Bare Exception with ValueError

**Files:**
- Modify: `Env/arithmeticEnv.py` (~11 locations)
- No new tests

**Interfaces:**
- Consumes: existing `ArithmeticEnv` class with all static methods
- Produces: same exceptions raised with same messages, but `ValueError` instead of `Exception`

- [ ] **Step 1: Find all bare Exception raises**

In `Env/arithmeticEnv.py`, search for `raise Exception(`. Expected ~11 occurrences in:
- `powerFun`
- `moduloFun`
- `ltFun`
- `gtFun`
- `eqFun`
- `neFun`
- `leFun`
- `geFun`
- `incrementFun`
- `decrementFun`
- `storeFun`

- [ ] **Step 2: Replace all with ValueError**

Replace every `raise Exception("` with `raise ValueError("`.

Full list of replacements:
```python
# powerFun
raise ValueError("power requires exactly two arguments")

# moduloFun
raise ValueError("modulo requires exactly two arguments")

# ltFun
raise ValueError("lt requires exactly two arguments")

# gtFun
raise ValueError("gt requires exactly two arguments")

# eqFun
raise ValueError("eq requires exactly two arguments")

# neFun
raise ValueError("ne requires exactly two arguments")

# leFun
raise ValueError("le requires exactly two arguments")

# geFun
raise ValueError("ge requires exactly two arguments")

# incrementFun
raise ValueError("increment requires exactly one argument")

# decrementFun
raise ValueError("decrement requires exactly one argument")

# storeFun
raise ValueError("Only One variable and one Integer is support")
```

- [ ] **Step 3: Verify with grep**

Run: `grep -n "raise Exception" Env/arithmeticEnv.py`
Expected: No output (all replaced).

- [ ] **Step 4: Run tests**

Run: `make test && make e2e`
Expected: All tests pass. `ValueError` is a subclass of `Exception`, so existing error handling in `javs.py` still catches it.

- [ ] **Step 5: Commit**

```bash
git add Env/arithmeticEnv.py
git commit -m "refactor: replace bare Exception with ValueError in ArithmeticEnv"
```

---

### Task 4: Fix F-string Spacing in addFun

**Files:**
- Modify: `Env/arithmeticEnv.py` (line 27)
- No new tests

**Interfaces:**
- Consumes: existing `ArithmeticEnv.addFun()`
- Produces: same return format with corrected spacing

- [ ] **Step 1: Find the f-string**

In `Env/arithmeticEnv.py`, line 27 contains:
```python
return f"result =int({' + '.join(parts)})"
```

- [ ] **Step 2: Add space after =**

Replace with:
```python
return f"result = int({' + '.join(parts)})"
```

- [ ] **Step 3: Run tests**

Run: `make test && make e2e`
Expected: All tests pass (spacing change only affects string format, not logic).

- [ ] **Step 4: Commit**

```bash
git add Env/arithmeticEnv.py
git commit -m "fix: add missing space in addFun result f-string"
```

---

### Task 5: Precompute env_Variables as Set

**Files:**
- Modify: `JAVS_Util/globalTape.py` (lines 24-30)
- No new tests

**Interfaces:**
- Consumes: existing `JAVGlobalTape.make()` signature
- Produces: same return type `np.ndarray`, same behavior, O(1) lookup instead of O(n)

- [ ] **Step 1: Read globalTape.py make() method**

Open `JAVS_Util/globalTape.py`, find the `make()` method starting at line 24.

Current relevant section (lines 24-30):
```python
    def make(
        tokenize_input: NDArray[np.str_],
        env: type[_EnvBase] | _EnvBase,
        show_logs: bool = False,
    ) -> np.ndarray:
        string_initial_constant = "$~"
        global_tape: list[NDArray[np.str_]] = []
        iterate_each_word = iter(tokenize_input)
```

- [ ] **Step 2: Add set conversion after docstring**

Insert after `string_initial_constant = "$~"` and before `global_tape`:
```python
        _env_vars_set: set[str] = set(str(v) for v in env.env_Variables)
```

- [ ] **Step 3: Replace NDArray membership test with set**

Find line 79:
```python
                    elif current_word in env.env_Variables:
```

Replace with:
```python
                    elif current_word in _env_vars_set:
```

- [ ] **Step 4: Run typecheck**

Run: `make typecheck`
Expected: Pass (no type changes).

- [ ] **Step 5: Run tests**

Run: `make test && make e2e`
Expected: All tests pass. Set conversion preserves all variable names.

- [ ] **Step 6: Commit**

```bash
git add JAVS_Util/globalTape.py
git commit -m "perf: precompute env_Variables as set for O(1) membership lookup"
```

---

### Task 6: Final Verification and Cleanup Commit

**Files:**
- No file changes
- Run: all make targets

**Interfaces:**
- Consumes: all previous tasks
- Produces: clean repo with all fixes applied

- [ ] **Step 1: Run full verification suite**

Run: `make lint && make typecheck && make test && make e2e`
Expected: All pass with zero errors.

- [ ] **Step 2: Run ruff --fix to auto-fix any remaining SIM issues**

Run: `ruff check . --fix`
Expected: May show additional auto-fixes; apply them.

- [ ] **Step 3: Commit any remaining fixes**

```bash
git add -A
git commit -m "fix: address remaining ruff SIM issues from auto-fix"
```

- [ ] **Step 4: Final verification**

Run: `make lint && make typecheck && make test && make e2e`
Expected: All pass.

- [ ] **Step 5: Push to remote**

Run: `git push origin master`
Expected: Success.
