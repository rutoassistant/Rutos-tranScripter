# Spec: Control Flow Support (if / else / for / while)

## Goal

Add `if`, `else`, `for` (repeat), and `while`/`until` to tranScripter as a new `ControlFlowEnv`, following the existing "word-as-function" pattern.

## Context

tranScripter currently only supports arithmetic. The architecture:
1. NLTK tokenizes `.ai` input into `NDArray[str]`
2. `RightHandTree` builds a per-sentence tree → `makeTape()` flattens to `NDArray[str]`
3. `Machine.generatePythonCode()` walks the tape **in reverse**, buffering non-function tokens and passing them to `env_Words_and_WordAsFunction` mappings
4. Generated Python strings are joined and `exec()`'d

Control flow requires hierarchical structure (condition + body), but the tape is currently flat. The fix: the machine performs a **forward scan** to detect block boundaries, extracts sub-tapes for conditions and bodies, then applies the existing reverse-walk logic to each sub-tape.

## Design

### New Environment: `ControlFlowEnv`

```python
class ControlFlowEnv(ArithmeticEnv):
    """Control flow environment — extends ArithmeticEnv with if/for/while."""
    
    name_of_Env: str = "ControlFlowEnv"
    
    # Condition helpers (also used by arithmetic)
    env_Words_and_WordAsFunction: ClassVar[dict[str, Callable[..., str | None]]] = {
        # --- condition words (inherited from ArithmeticEnv) ---
        # eq, ne, gt, lt, ge, le already defined in ArithmeticEnv
        
        # --- block markers ---
        "if": ifFun,
        "then": thenFun,
        "else": elseFun,
        "end_if": endIfFun,
        "endif": endIfFun,
        
        # --- counted loops ---
        "repeat": repeatFun,
        "times": timesFun,
        "end_repeat": endRepeatFun,
        "endrepeat": endRepeatFun,
        
        # --- iteration loops ---
        "for": forFun,
        "each": eachFun,
        "in": inFun,  # override: ControlFlowEnv uses 'in' for loop context
        "end_for": endForFun,
        "endfor": endForFun,
        
        # --- conditional loops ---
        "while": whileFun,
        "until": untilFun,
        "end_while": endWhileFun,
        "endwhile": endWhileFun,
        
        # --- boolean operators ---
        "not": notFun,
        "and": andFun,   # override: ControlFlowEnv uses 'and' for conditions
        "or": orFun,
    }
```

#### Function Signatures

All functions follow the `*args: str → str | None` pattern. Args are the buffered tokens from the reverse walk.

| Function | Args | Returns |
|---|---|---|
| `ifFun(*args)` | `[condition_str]` | `"if {condition}:"` |
| `thenFun(*args)` | — | `None` |
| `elseFun(*args)` | — | `"else:"` |
| `endIfFun(*args)` | — | `""` (triggers dedent) |
| `repeatFun(*args)` | `[n]` | `"for _javs_repeat_{n} in range({n}):"` |
| `timesFun(*args)` | — | `None` |
| `endRepeatFun(*args)` | — | `""` (triggers dedent) |
| `forFun(*args)` | `[var, collection]` | `"for {var} in {collection}:"` |
| `eachFun(*args)` | — | `None` |
| `inFun(*args)` | — | `None` |
| `endForFun(*args)` | — | `""` (triggers dedent) |
| `whileFun(*args)` | `[condition_str]` | `"while {condition}:"` |
| `untilFun(*args)` | `[condition_str]` | `"while not {condition}:"` |
| `endWhileFun(*args)` | — | `""` (triggers dedent) |
| `notFun(*args)` | `[expr]` | `"not {expr}"` |
| `andFun(*args)` | `[left, right]` | `"{left} and {right}"` |
| `orFun(*args)` | `[left, right]` | `"{left} or {right}"` |

### Machine Changes

`machine.py` `generatePythonCode()` gains a **forward-scan mode** when control flow keywords are detected. The input `global_tape` is a 2D structure: `list[NDArray[str]]` (one tape per sentence). The machine iterates sentences, and within each sentence, scans forward for block markers.

```python
def generatePythonCode(self, global_tape: list[np.ndarray], env: type[_EnvBase] | _EnvBase) -> list[str]:
    lines: list[str] = []
    for sentence_tape in global_tape:
        lines.extend(self._process_sentence(sentence_tape, env))
    return lines

def _process_sentence(self, sentence_tape: np.ndarray, env, indent_level: int = 0) -> list[str]:
    """Forward-scan a single sentence's tape for block structures."""
    ...
```

Helper `_extract_block(sentence_tape, start_index, env)` scans forward from `start_index` to find the matching end keyword (`end_if`, `end_repeat`, etc.) or colon delimiter. Returns `(block_tape_slice, end_index)`.

Helper `_split_block(block_tape)` separates condition portion (before body keywords like `store`, `print`) from body portion. Uses `env.block_body_keywords` to identify where the body begins.

Helper `_generate_code_segment(tape_segment, env, indent_level)` is the **existing** reverse-walk logic, extracted into a standalone method for reuse on condition/body sub-tapes.

### Tape Format

The tape remains `NDArray[object]` (mixed types). Simple tokens stay as strings. Block references use tuple markers:

```python
# Simple statement
tape = np.array(["add", "3", "with", "5"], dtype=object)

# With control flow (block markers)
tape = np.array([
    "if",
    "x", "is", "greater", "than", "5",   # condition segment
    "store", "10", "in", "$v1",          # body segment
    "end_if",
], dtype=object)
```

The machine's forward scan identifies block boundaries and splits segments automatically — the user doesn't need to manually format the tape.

### Supported English Sentence Patterns

All patterns use the `.ai` file format (one sentence per line, ending with `.`). Colons (`:`) separate conditions from bodies in single-line sentences. Multi-line sentences use explicit `end_if`/`end_repeat`/`end_while` markers.

| Pattern | Example `.ai` input | Generated Python |
|---|---|---|
| `if` / `then` / `end if` | `if x is greater than 5: store 10 in $v1` | `if x > 5:\n    v1 = 10` |
| `if` / `else` / `end if` | `if x is greater than 5: store 10 in $v1 else: store 20 in $v1` | `if x > 5:\n    v1 = 10\nelse:\n    v1 = 20` |
| `repeat` / `times` | `repeat 10 times: print result` | `for _javs_repeat_10 in range(10):\n    print(result,)` |
| `for` / `each` / `in` | `for each item in my_list: print item` | `for item in my_list:\n    print(item,)` |
| `while` | `while x is less than 10: increment x` | `while x < 10:\n    result = x + 1` |
| `until` | `until x is greater than 100: multiply x with 2` | `while not x > 100:\n    result = x * 2` |
| `not` (negation) | `if x is not equal to 0: print x` | `if x != 0:\n    print(x,)` |
| `and` (compound) | `if x is greater than 0 and x is less than 10: store 1 in $v1` | `if x > 0 and x < 10:\n    v1 = 1` |
| `or` (compound) | `if x is equal to 0 or x is equal to 1: store 2 in $v1` | `if x == 0 or x == 1:\n    v1 = 2` |
| Nested if/for | `if x is greater than 0: repeat 3 times: store x in $v1` | `if x > 0:\n    for _javs_repeat_3 in range(3):\n        v1 = x` |

### Files to Change

| File | Change |
|---|---|
| `Env/controlFlowEnv.py` | **new** — `ControlFlowEnv` class |
| `JAVS_Util/machine.py` | Extract reverse-walk to `_generate_code_segment()`, add forward-scan block detection |
| `javs.py` | Wire `ControlFlowEnv` alongside `ArithmeticEnv` |
| `test_arithmetic_env.py` | Add control flow unit tests |
| `test_e2e.py` | Add e2e test cases |
| `README.md` | Document new syntax |

### Testing Strategy

1. **Unit tests** — each `ControlFlowEnv` function tested in isolation
2. **Integration tests** — full sentences parsed end-to-end, verified Python output matches expected
3. **Edge cases** — nested if/for, empty bodies, malformed conditions

### Out of Scope (Future)

- `break` / `continue`
- `try` / `except`
- Function definitions (`def`)
- Multiple conditions in one sentence without `and`/`or`
- `elif`
