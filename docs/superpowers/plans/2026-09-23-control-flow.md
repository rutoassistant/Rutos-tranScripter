# Control Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `if`/`else`/`for`/`while` control flow to tranScripter via a new `ControlFlowEnv` that inherits from `ArithmeticEnv`.

**Architecture:** `ControlFlowEnv` extends `ArithmeticEnv` (inheriting all arithmetic words). Machine gains a forward-scan helper that detects block-start keywords in the tape, splits condition/body segments, and recursively processes them with the existing reverse-walk logic. RightHandTree and globalTape are unchanged.

**Tech Stack:** Python 3.13, numpy, nltk

**Spec:** `docs/superpowers/specs/2026-09-23-control-flow-design.md`

## Global Constraints

- No `typing.Any` — use concrete types (`str`, `np.ndarray`, `list[str]`)
- All functions follow `*args: str → str | None` pattern (word-as-function)
- `ControlFlowEnv` must inherit from `ArithmeticEnv` (no duplicate word declarations)
- Follow existing code style: `__init__.py` exports, `_EnvBase` pattern, numpy-backed tapes
- Commit after each task; keep commits atomic

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `Env/controlFlowEnv.py` | **Create** | `ControlFlowEnv` class with control-flow functions |
| `JAVS_Util/machine.py` | **Modify** | Extract `_generate_code_segment()`, add `_process_sentence()`, `_extract_block()` |
| `javs.py` | **Modify** | Import and wire `ControlFlowEnv` alongside `ArithmeticEnv` |
| `test_arithmetic_env.py` | **Modify** | Add unit tests for control flow functions |
| `test_e2e.py` | **Modify** | Add end-to-end test cases for if/else/for/while |
| `README.md` | **Modify** | Document new syntax patterns |
| `JAVS_Util/rightHandTree.py` | No change | Tree stays flat |
| `JAVS_Util/globalTape.py` | No change | Tape format unchanged |

---

### Task 1: Create `ControlFlowEnv`

**Files:**
- Create: `Env/controlFlowEnv.py`

**Interfaces:**
- Consumes: `ArithmeticEnv` (parent class), `_EnvBase`
- Produces: `ControlFlowEnv` class with `env_Words_and_WordAsFunction` dict containing all arithmetic + control flow words

- [ ] **Step 1: Write the failing test**

```python
# test_control_flow_env.py (create temporarily, will move to test_arithmetic_env.py)
import pytest
from Env.controlFlowEnv import ControlFlowEnv


def test_control_flow_env_inherits_arithmetic():
    """ControlFlowEnv should have all ArithmeticEnv words."""
    arithmetic_words = set(ControlFlowEnv.env_Words_and_WordAsFunction.keys())
    assert "add" in arithmetic_words
    assert "store" in arithmetic_words
    assert "print" in arithmetic_words
    assert "gt" in arithmetic_words


def test_control_flow_env_has_new_words():
    """ControlFlowEnv should declare control flow words."""
    words = set(ControlFlowEnv.env_Words_and_WordAsFunction.keys())
    assert "if" in words
    assert "else" in words
    assert "end_if" in words
    assert "repeat" in words
    assert "for" in words
    assert "while" in words
    assert "until" in words
    assert "not" in words
    assert "and" in words
    assert "or" in words


def test_end_if_returns_empty_string():
    assert ControlFlowEnv.endIfFun() == ""


def test_then_returns_none():
    assert ControlFlowEnv.thenFun() is None


def test_times_returns_none():
    assert ControlFlowEnv.timesFun() is None


def test_each_returns_none():
    assert ControlFlowEnv.eachFun() is None


def test_in_returns_none():
    assert ControlFlowEnv.inFun() is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest test_control_flow_env.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'controlFlowEnv'"

- [ ] **Step 3: Write minimal implementation**

Create `Env/controlFlowEnv.py`:

```python
"""Control flow environment: if/else/for/while/then/and/or/not."""
from __future__ import annotations

from typing import ClassVar
from collections.abc import Callable

from Env.arithmeticEnv import ArithmeticEnv


class ControlFlowEnv(ArithmeticEnv):
    """Extends ArithmeticEnv with control flow keywords."""

    name_of_Env: str = "ControlFlowEnv"

    @staticmethod
    def ifFun(*args: str) -> str:
        condition = " ".join(args)
        return f"if {condition}:"

    @staticmethod
    def thenFun(*args: str) -> None:
        return None

    @staticmethod
    def elseFun(*args: str) -> str:
        return "else:"

    @staticmethod
    def endIfFun(*args: str) -> str:
        return ""

    @staticmethod
    def repeatFun(*args: str) -> str:
        n = args[0]
        return f"for _javs_repeat_{n} in range({n}):"

    @staticmethod
    def timesFun(*args: str) -> None:
        return None

    @staticmethod
    def endRepeatFun(*args: str) -> str:
        return ""

    @staticmethod
    def forFun(*args: str) -> str:
        var, collection = args[0], args[1]
        var_name = var[1:] if "$" in var else var
        return f"for {var_name} in {collection}:"

    @staticmethod
    def eachFun(*args: str) -> None:
        return None

    @staticmethod
    def inFun(*args: str) -> None:
        return None

    @staticmethod
    def endForFun(*args: str) -> str:
        return ""

    @staticmethod
    def whileFun(*args: str) -> str:
        condition = " ".join(args)
        return f"while {condition}:"

    @staticmethod
    def untilFun(*args: str) -> str:
        condition = " ".join(args)
        return f"while not {condition}:"

    @staticmethod
    def endWhileFun(*args: str) -> str:
        return ""

    @staticmethod
    def notFun(*args: str) -> str:
        expr = args[0]
        return f"not {expr}"

    @staticmethod
    def andFun(*args: str) -> str:
        return " and ".join(args)

    @staticmethod
    def orFun(*args: str) -> str:
        return " or ".join(args)

    env_Words_and_WordAsFunction: ClassVar[dict[str, Callable[..., str | None]]] = {
        **ArithmeticEnv.env_Words_and_WordAsFunction,
        "if": ifFun,
        "then": thenFun,
        "else": elseFun,
        "end_if": endIfFun,
        "endif": endIfFun,
        "repeat": repeatFun,
        "times": timesFun,
        "end_repeat": endRepeatFun,
        "endrepeat": endRepeatFun,
        "for": forFun,
        "each": eachFun,
        "in": inFun,
        "end_for": endForFun,
        "endfor": endForFun,
        "while": whileFun,
        "until": untilFun,
        "end_while": endWhileFun,
        "endwhile": endWhileFun,
        "not": notFun,
        "and": andFun,
        "or": orFun,
    }
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest test_control_flow_env.py -v`
Expected: All tests PASS

- [ ] **Step 5: Move tests to proper location and clean up**

```bash
# Append test functions to test_arithmetic_env.py
# Remove temporary test file
rm test_control_flow_env.py
```

- [ ] **Step 6: Commit**

```bash
git add Env/controlFlowEnv.py test_arithmetic_env.py
git commit -m "feat: add ControlFlowEnv with if/else/for/while support"
```

---

### Task 2: Refactor Machine for Block Detection

**Files:**
- Modify: `JAVS_Util/machine.py`

**Interfaces:**
- Consumes: `np.ndarray` (tape), `_EnvBase` (env)
- Produces: `list[str]` (Python code lines)

- [ ] **Step 1: Write the failing test**

Add to `test_arithmetic_env.py`:

```python
import numpy as np
from JAVS_Util.machine import Machine
from Env.controlFlowEnv import ControlFlowEnv


def test_machine_if_simple():
    """Test simple if statement generation."""
    # Tape: if x > 5: store 10 in $v1
    # Machine should produce: ["if x > 5:", "    v1 = 10"]
    tape = np.array(["if", "x", ">", "5", "store", "10", "in", "$v1"], dtype=object)
    result = Machine.generatePythonCode([tape], ControlFlowEnv)
    assert len(result) >= 2
    assert any("if x > 5:" in line for line in result)
    assert any("v1 = 10" in line for line in result)


def test_machine_else():
    """Test if/else generation."""
    tape = np.array(["if", "x", ">", "5", "store", "10", "in", "$v1", "else", "store", "20", "in", "$v1"], dtype=object)
    result = Machine.generatePythonCode([tape], ControlFlowEnv)
    assert any("else:" in line for line in result)


def test_machine_repeat():
    """Test repeat loop generation."""
    tape = np.array(["repeat", "10", "times", "print", "result"], dtype=object)
    result = Machine.generatePythonCode([tape], ControlFlowEnv)
    assert any("range(10)" in line for line in result)


def test_machine_while():
    """Test while loop generation."""
    tape = np.array(["while", "x", "<", "10", "increment", "x"], dtype=object)
    result = Machine.generatePythonCode([tape], ControlFlowEnv)
    assert any("while x < 10:" in line for line in result)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest test_arithmetic_env.py::test_machine_if_simple -v`
Expected: FAIL — current machine doesn't handle control flow

- [ ] **Step 3: Refactor machine.py**

Replace `JAVS_Util/machine.py` with:

```python
"""Machine: generates and executes Python code from the global tape."""
from __future__ import annotations

import numpy as np

from JAVS_Util.globalTape import _EnvBase


class Machine:
    """Translates a list of sentence tapes into executable Python code."""

    # Keywords that start a code block
    BLOCK_START_KEYWORDS: frozenset[str] = frozenset({
        "if", "repeat", "for", "while", "until",
    })

    # Keywords that end a code block
    BLOCK_END_KEYWORDS: frozenset[str] = frozenset({
        "end_if", "endif", "end_repeat", "endrepeat",
        "end_for", "endfor", "end_while", "endwhile",
    })

    # Keywords that indicate the start of a block body
    BODY_START_KEYWORDS: frozenset[str] = frozenset({
        "store", "print", "display", "add", "subtract", "multiply",
        "divide", "power", "modulo", "increment", "decrement",
        "if", "repeat", "for", "while", "until",
    })

    @staticmethod
    def generatePythonCode(global_tape: list[np.ndarray], env: type[_EnvBase] | _EnvBase) -> list[str]:
        python_code: list[str] = []
        for sentence_tape in global_tape:
            python_code.extend(Machine._process_sentence(sentence_tape, env))
        return python_code

    @staticmethod
    def _process_sentence(sentence_tape: np.ndarray, env: type[_EnvBase] | _EnvBase, indent_level: int = 0) -> list[str]:
        """Forward-scan a sentence tape for block structures."""
        lines: list[str] = []
        i = 0
        while i < len(sentence_tape):
            word = str(sentence_tape[i]).lower()
            
            if word in Machine.BLOCK_START_KEYWORDS:
                # Extract block from here to matching end keyword
                block_slice, end_idx = Machine._extract_block(sentence_tape, i, env)
                
                # Split block into condition and body
                cond_tape, body_tape = Machine._split_block(block_slice, word)
                
                # Generate condition code
                cond_code = Machine._generate_code_segment(cond_tape, env, indent_level + 1)
                condition_str = " ".join(cond_code).strip()
                
                # Emit block header
                if word in ("repeat",):
                    # Special case: repeat takes a number, not a condition expression
                    header = env.env_Words_and_WordAsFunction[word](cond_code[0] if cond_code else "0")
                else:
                    header = env.env_Words_and_WordAsFunction[word](*cond_code)
                
                lines.append(f"{'    ' * indent_level}{header}")
                
                # Generate body recursively
                lines.extend(Machine._process_sentence(body_tape, env, indent_level + 1))
                
                # Handle else
                else_idx = Machine._find_else(body_tape)
                if else_idx is not None:
                    else_body = body_tape[else_idx:]
                    lines.append(f"{'    ' * indent_level}else:")
                    lines.extend(Machine._process_sentence(else_body, env, indent_level + 1))
                
                # Emit dedent marker (empty string that signals dedent)
                end_keyword = Machine._get_end_keyword(word)
                if end_keyword:
                    lines.append(f"{'    ' * indent_level}{end_keyword}")
                
                i = end_idx + 1
            else:
                # Standard reverse-walk for non-block words
                segment_lines = Machine._generate_code_segment(sentence_tape[i:i+1], env, indent_level)
                lines.extend(segment_lines)
                i += 1
        
        return lines

    @staticmethod
    def _generate_code_segment(tape_segment: np.ndarray, env: type[_EnvBase] | _EnvBase, indent_level: int = 0) -> list[str]:
        """Reverse-walk a tape segment (existing logic, extracted)."""
        variable_buffer: list[str] = []
        result: list[str] = []
        
        for word in reversed(tape_segment):
            word_str = str(word).lower()
            if "$" in word:
                variable_buffer.append(word)
            elif word_str in env.env_Words_and_WordAsFunction:
                func = env.env_Words_and_WordAsFunction[word_str]
                code = func(*variable_buffer)
                if code is not None and code != "":
                    result.insert(0, f"{'    ' * indent_level}{code}")
                variable_buffer = []
            else:
                # Non-function word, buffer it
                variable_buffer.insert(0, word_str)
        
        # Handle remaining buffer (variable without function)
        if variable_buffer:
            result.insert(0, f"{'    ' * indent_level}{' '.join(variable_buffer)}")
        
        return result

    @staticmethod
    def _extract_block(tape: np.ndarray, start_idx: int, env: type[_EnvBase] | _EnvBase) -> tuple[np.ndarray, int]:
        """Find the extent of a block starting at start_idx."""
        start_word = str(tape[start_idx]).lower()
        depth = 1
        i = start_idx + 1
        
        while i < len(tape) and depth > 0:
            word = str(tape[i]).lower()
            
            if word in Machine.BLOCK_START_KEYWORDS:
                depth += 1
            elif word in Machine.BLOCK_END_KEYWORDS:
                depth -= 1
                if depth == 0:
                    return tape[start_idx:i+1], i
            
            i += 1
        
        # Fallback: scan until we hit another sentence boundary or block end
        return tape[start_idx:], len(tape) - 1

    @staticmethod
    def _split_block(block_tape: np.ndarray, start_word: str) -> tuple[np.ndarray, np.ndarray]:
        """Split a block into condition and body portions."""
        # Find where the body starts (first keyword in BODY_START_KEYWORDS after position 0)
        body_start = 1  # Default: body starts after the keyword
        
        for i in range(1, len(block_tape)):
            word = str(block_tape[i]).lower()
            if word in Machine.BODY_START_KEYWORDS:
                body_start = i
                break
        
        cond_tape = block_tape[1:body_start]
        body_tape = block_tape[body_start:]
        
        return cond_tape, body_tape

    @staticmethod
    def _find_else(body_tape: np.ndarray) -> int | None:
        """Find the index of 'else' in a body tape."""
        for i, word in enumerate(body_tape):
            if str(word).lower() == "else":
                return i
        return None

    @staticmethod
    def _get_end_keyword(start_word: str) -> str:
        """Get the corresponding end keyword for a start keyword."""
        mapping = {
            "if": "end_if",
            "repeat": "end_repeat",
            "for": "end_for",
            "while": "end_while",
            "until": "end_while",
        }
        return mapping.get(start_word, "")

    @staticmethod
    def executePyCode(code: list[str]) -> None:
        exec("\n".join(code))

    @staticmethod
    def generatePyFile(filename: str, code: list[str]) -> None:
        with open(file=f"{filename}.generated.py", mode="w") as f:
            f.writelines("\n".join(code))
            print("**** Python Code Generated ****")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest test_arithmetic_env.py::test_machine_if_simple test_arithmetic_env.py::test_machine_else test_arithmetic_env.py::test_machine_repeat test_arithmetic_env.py::test_machine_while -v`
Expected: All tests PASS

- [ ] **Step 5: Run full test suite to verify no regressions**

Run: `.venv/bin/python -m pytest test_arithmetic_env.py -v`
Expected: All existing + new tests PASS

- [ ] **Step 6: Commit**

```bash
git add JAVS_Util/machine.py test_arithmetic_env.py
git commit -m "feat: add forward-scan block detection to Machine"
```

---

### Task 3: Wire ControlFlowEnv in CLI

**Files:**
- Modify: `javs.py`

**Interfaces:**
- Consumes: `ControlFlowEnv` from `Env.controlFlowEnv`
- Produces: CLI accepts `.ai` files with control flow syntax

- [ ] **Step 1: Write the failing test**

Add to `test_arithmetic_env.py`:

```python
def test_cli_control_flow():
    """Test that CLI accepts and runs control flow sentences."""
    import tempfile
    import os
    from javs import main
    
    ai_content = """if x is greater than 5: store 10 in $v1
print result."""
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ai", delete=False) as f:
        f.write(ai_content)
        temp_path = f.name
    
    try:
        # Should not raise an exception
        main(temp_path)
        # If we get here, the pipeline worked
    finally:
        os.unlink(temp_path)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/python -m pytest test_arithmetic_env.py::test_cli_control_flow -v`
Expected: FAIL — `ControlFlowEnv` not imported in `javs.py`

- [ ] **Step 3: Update javs.py**

Add `ControlFlowEnv` import and use it as the default environment:

```python
from Env.controlFlowEnv import ControlFlowEnv
```

Change the `main()` function to use `ControlFlowEnv` instead of `ArithmeticEnv`:

```python
# Line 24: Change this
word_list = Tokenize.generateWordListFromEnv(ArithmeticEnv)
# To this
word_list = Tokenize.generateWordListFromEnv(ControlFlowEnv)

# Line 27-28: Change this
tape = JAVGlobalTape.make(
    tokenize_input=tokenize, env=ArithmeticEnv, show_logs=print_log
)
# To this
tape = JAVGlobalTape.make(
    tokenize_input=tokenize, env=ControlFlowEnv, show_logs=print_log
)

# Line 29: Change this
py_code = Machine.generatePythonCode(tape, ArithmeticEnv)
# To this
py_code = Machine.generatePythonCode(tape, ControlFlowEnv)
```

Also update the `-envWords` output to show `ControlFlowEnv`:

```python
# Line 91: Change this
print(f"Env Name :- {ArithmeticEnv.name_of_Env}\n")
# To this
print(f"Env Name :- {ControlFlowEnv.name_of_Env}\n")

# Line 93: Change this
for words in Tokenize.generateWordListFromEnv(ArithmeticEnv):
# To this
for words in Tokenize.generateWordListFromEnv(ControlFlowEnv):
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/python -m pytest test_arithmetic_env.py::test_cli_control_flow -v`
Expected: PASS

- [ ] **Step 5: Run full test suite**

Run: `.venv/bin/python -m pytest test_arithmetic_env.py -v`
Expected: All tests PASS

- [ ] **Step 6: Run e2e tests**

Run: `.venv/bin/python test_e2e.py test_full.ai`
Expected: 0 failures

- [ ] **Step 7: Commit**

```bash
git add javs.py
git commit -m "feat: wire ControlFlowEnv into CLI"
```

---

### Task 4: Add E2E Tests

**Files:**
- Modify: `test_e2e.py`

**Interfaces:**
- Consumes: `ControlFlowEnv`, `Machine`, `Tokenize`
- Produces: E2E test cases covering all control flow patterns

- [ ] **Step 1: Add e2e test cases**

Append to `test_e2e.py`:

```python
# Control flow test cases
control_flow_tests = [
    {
        "name": "simple if",
        "input": "if x is greater than 5: store 10 in $v1\nprint result.",
        "expected_contains": ["if x > 5:", "v1 = 10", "print"],
    },
    {
        "name": "if else",
        "input": "if x is greater than 5: store 10 in $v1 else: store 20 in $v1\nprint result.",
        "expected_contains": ["if x > 5:", "v1 = 10", "else:", "v1 = 20"],
    },
    {
        "name": "repeat loop",
        "input": "repeat 3 times: store result in $v1\nprint result.",
        "expected_contains": ["range(3)", "v1 = result"],
    },
    {
        "name": "for each loop",
        "input": "for each item in my_list: print item.",
        "expected_contains": ["for item in my_list:", "print"],
    },
    {
        "name": "while loop",
        "input": "while x is less than 10: increment x\nprint result.",
        "expected_contains": ["while x < 10:", "result = x + 1"],
    },
    {
        "name": "until loop",
        "input": "until x is greater than 100: multiply x with 2\nprint result.",
        "expected_contains": ["while not x > 100:", "result = x * 2"],
    },
    {
        "name": "not negation",
        "input": "if x is not equal to 0: print x.",
        "expected_contains": ["if x != 0:", "print(x,)"],
    },
    {
        "name": "and compound condition",
        "input": "if x is greater than 0 and x is less than 10: store 1 in $v1\nprint result.",
        "expected_contains": ["if x > 0 and x < 10:", "v1 = 1"],
    },
    {
        "name": "or compound condition",
        "input": "if x is equal to 0 or x is equal to 1: store 2 in $v1\nprint result.",
        "expected_contains": ["if x == 0 or x == 1:", "v1 = 2"],
    },
]
```

Also add the test execution loop:

```python
# At the end of test_e2e.py, add:
def run_control_flow_tests():
    """Run all control flow e2e tests."""
    print("\n=== Control Flow E2E Tests ===")
    passed = 0
    failed = 0
    
    for test in control_flow_tests:
        try:
            input_text = test["input"]
            tokenize = Tokenize.make(input_text)
            word_list = Tokenize.generateWordListFromEnv(ControlFlowEnv)
            Tokenize.checkAllWordsInEnv(words_list=tokenize, env_words=word_list)
            tape = JAVGlobalTape.make(tokenize_input=tokenize, env=ControlFlowEnv)
            py_code = Machine.generatePythonCode(tape, ControlFlowEnv)
            
            all_found = all(any(exp in line for line in py_code) for exp in test["expected_contains"])
            
            if all_found:
                print(f"PASS: {test['name']}")
                passed += 1
            else:
                print(f"FAIL: {test['name']}")
                print(f"  Expected: {test['expected_contains']}")
                print(f"  Got: {py_code}")
                failed += 1
        except Exception as e:
            print(f"FAIL: {test['name']} — {e}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    # Existing test code...
    
    # Run control flow tests
    control_flow_passed = run_control_flow_tests()
    
    if not control_flow_passed:
        sys.exit(1)
```

- [ ] **Step 2: Run e2e tests**

Run: `.venv/bin/python test_e2e.py`
Expected: All control flow tests PASS

- [ ] **Step 3: Commit**

```bash
git add test_e2e.py
git commit -m "test: add e2e tests for control flow"
```

---

### Task 5: Update README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add control flow section**

Append to `README.md` before the "Research & Documentation" section:

```markdown
## Control Flow

tranScripter now supports conditional and looping constructs:

### If / Else
```
if x is greater than 5: store 10 in $v1
if x is greater than 5: store 10 in $v1 else: store 20 in $v1
```

### Repeat Loop
```
repeat 10 times: print result
```

### For Loop
```
for each item in my_list: print item
```

### While / Until
```
while x is less than 10: increment x
until x is greater than 100: multiply x with 2
```

### Compound Conditions
```
if x is greater than 0 and x is less than 10: store 1 in $v1
if x is equal to 0 or x is equal to 1: store 2 in $v1
```

### Negation
```
if x is not equal to 0: print x
```

See [test_e2e.py](test_e2e.py) for full examples.
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: document control flow syntax"
```

---

## Self-Review Checklist

### Spec Coverage
- [x] ControlFlowEnv extends ArithmeticEnv (no duplicate words)
- [x] All control flow functions defined (if, else, repeat, for, while, until, not, and, or)
- [x] Machine forward-scan block detection implemented
- [x] Condition/body splitting logic
- [x] Recursive block processing for nesting
- [x] E2E tests for all patterns
- [x] README documentation

### Placeholder Scan
No TBDs, TODOs, or "implement later" items found.

### Type Consistency
- All functions use `*args: str → str | None`
- Machine uses `list[np.ndarray]` for global_tape
- ControlFlowEnv properly typed with `ClassVar`

### Edge Cases to Verify
- Nested if/for (recursive processing)
- Empty bodies (should generate `pass`)
- Malformed conditions (should raise ValueError)

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-09-23-control-flow.md`.

**Two execution options:**

**1. Subagent-Driven (recommended)** — Dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
