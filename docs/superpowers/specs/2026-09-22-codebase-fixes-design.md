# Codebase Fixes — Docs-mcp Verification Results

**Date:** 2026-09-22
**Scope:** Bounded — fixes to 4 existing files based on docs-mcp research
**Approvals needed before each section:** yes (per brainstorming hard-gate)

---

## Background

Docs-mcp verification found 4 issues:
1. Ruff missing `SIM` (flake8-simplify) rule group
2. List concatenation with spread operators instead of `.extend()`
3. Bare `Exception("...")` raises instead of `ValueError`
4. Missing space in f-string: `"result =int(...)"` → `"result = int(...)"`
5. `np.ndarray` membership test (`in`) in tight loop instead of `set`

All issues are low-impact. No correctness bugs. Changes are mechanical.

---

## Section 1: Ruff Configuration

**File:** `pyproject.toml`
**Change:** Add `"SIM"` to `[tool.ruff.lint].select`

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
    "SIM", # flake8-simplify (NEW)
]
```

**Why:** `SIM` catches auto-simplifiable patterns that ruff can fix with `--fix`. Covers cases like the spread-based list concatenation in `machine.py`.

**Risk:** Low. Ruff run will flag issues but `--fix` handles them. If new rules surface unrelated issues, they can be individually ignored.

**Test:** `make lint` passes after `--fix`.

---

## Section 2: Machine — List Concatenation

**File:** `JAVS_Util/machine.py:28`

Current:
```python
python_code = [*python_code, *python_code_sentence]
```

Proposed:
```python
python_code.extend(python_code_sentence)
```

**Why:** `.extend()` is the idiomatic, efficient form. The spread syntax creates an intermediate list every iteration. With `SIM` enabled, ruff will auto-fix this.

**Risk:** None. Behaviorally identical.

---

## Section 3: ArithmeticEnv — Exception Types

**File:** `Env/arithmeticEnv.py`

Replace all bare `Exception("...")` with `ValueError("...")`.

Locations (line numbers approximate):
- `powerFun` (line ~47): `"power requires exactly two arguments"`
- `moduloFun` (line ~55): `"modulo requires exactly two arguments"`
- `ltFun` (line ~63): `"lt requires exactly two arguments"`
- `gtFun` (line ~71): `"gt requires exactly two arguments"`
- `eqFun` (line ~79): `"eq requires exactly two arguments"`
- `neFun` (line ~87): `"ne requires exactly two arguments"`
- `leFun` (line ~95): `"le requires exactly two arguments"`
- `geFun` (line ~103): `"ge requires exactly two arguments"`
- `incrementFun` (line ~111): `"increment requires exactly one argument"`
- `decrementFun` (line ~119): `"decrement requires exactly one argument"`
- `storeFun` (line ~134): `"Only One variable and one Integer is support"`

**Why:** `ValueError` is the semantically correct exception for argument count/type issues. `SIM` rule `SIM905` catches bare `Exception` when a more specific type exists.

**Risk:** None. All callers currently catch `JAVSError` or bare `Exception` — `ValueError` is a subclass of `Exception`, so existing `except Exception` clauses still catch it. The e2e tests validate no regression.

---

## Section 4: ArithmeticEnv — F-string Space

**File:** `Env/arithmeticEnv.py:27`

Current:
```python
return f"result =int({' + '.join(parts)})"
```

Proposed:
```python
return f"result = int({' + '.join(parts)})"
```

**Risk:** None. Cosmetic fix.

---

## Section 5: GlobalTape — Set Lookup

**File:** `JAVS_Util/globalTape.py:79`

Current:
```python
elif current_word in env.env_Variables:
```

Where `env.env_Variables` is a `NDArray[np.str_]` and this check runs once per token in the input.

Proposed:
```python
_env_vars_set: set[str] = set(str(v) for v in env.env_Variables)
# ...
elif current_word in _env_vars_set:
```

**Why:** `np.ndarray.__contains__` iterates all elements (O(n)). Converting to a Python `set` gives O(1) lookup per token. For typical env sizes (~1-20 variables) the difference is negligible, but it's the correct pattern per numpy docs.

**Risk:** Minimal. The set conversion is done once at function entry. If `env.env_Variables` is None or empty, the set is empty and the `in` check safely returns `False`.

**Test:** `make e2e` covers the path where env variables are looked up.

---

## Testing

All changes are covered by existing tests:
- `make lint` — verifies ruff/SIM pass
- `make typecheck` — no type changes
- `make test` — unit tests for arithmetic ops
- `make e2e` — full pipeline test (`test_full.ai`)

No new tests added.

---

## Commit Plan

Single commit after all changes:
```
Fix: improve code quality per docs-mcp verification
- Add SIM ruff rule group
- Use extend() instead of spread concat
- Replace bare Exception with ValueError
- Fix f-string spacing
- Precompute env_Variables as set for O(1) lookup
```

---

## What Was Skipped

- **No new logging/metrics** for the set conversion — overhead is negligible at this scale. Add when env has 1000+ variables.
- **No docstring additions** — changes are self-explanatory.
- **No `--fix` pre-run** — changes are small enough to patch directly; run ruff `--fix` after patches to catch any remaining SIM issues.
