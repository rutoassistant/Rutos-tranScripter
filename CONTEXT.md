# Project Context

## What This Is

JAVS-tranScripter is a research-based natural-language-to-Python transpiler. It accepts sentences written in a controlled subset of English (`.ai` files) and compiles them into executable Python statements. The project is **not production-grade** — it is a research prototype.

## Core Architecture

```
.ai file (natural language)
    → javs.py (main entry point)
        → JAVS_Util/tokenize.py (NLTK-based tokenizer + POS tagger)
        → JAVS_Util/globalTape.py (sentence tape — builds ordered token stream)
        → JAVS_Util/machine.py (Machine — walks the tape, dispatches to Environment functions)
        → Env/arithmeticEnv.py (ArithmeticEnv — maps words to Python code generators)
        → Generated Python code (executed or printed with -p)
```

### Key Design Points

- **Environments are pluggable.** Each Environment is a class with `env_Words_and_WordAsFunction` dict mapping words → static methods that return Python code strings. Currently only `ArithmeticEnv` exists.
- **The tape reverses operands.** `machine.py` iterates `reversed(sentenceTape)`, so functions like `subtractFun`, `divideFun`, `powerFun`, and `moduloFun` must internally reverse their args to produce correct operand order. `addFun` and `multiplyFun` are commutative and don't need reversal. Compare operations (`lt/gt/le/ge`) preserve natural order.
- **Variables use `$` prefix.** `$v1` in `.ai` becomes `v1` in generated Python. String literals use `~` prefix (e.g. `~hello` → `"hello"`).

## Current State (as of 2026-09-18)

### What Works

- 12 arithmetic operations: add, subtract, multiply, divide, power, modulo, lt, gt, eq, ne, le, ge
- Increment / decrement
- Variable storage and retrieval
- String literal printing
- Multi-statement sentences with `then`, `and`, `,`

### What's Tested

- `test_arithmetic_env.py` — 16 unit tests, all passing
- `test_e2e.py` — end-to-end runner, transpiles + executes `.ai` files
- `test_full.ai` — 15-operation integration test, all outputs verified correct
- CI runs on Alpine Linux via GitHub Actions (`.github/workflows/ci.yml`)

### What's Broken / Known Issues

- The transpiler is **not** a general-purpose NLP system. It works on a controlled grammar — sentences must follow specific patterns. Out-of-pattern sentences will fail or produce incorrect code.
- No error recovery for malformed input beyond basic tokenization checks.
- No Windows binary distribution (pure Python — runs from source).

## Research Foundations

This project is built on two prior works:

1. **"Artificial Level Language: A Library of Computing Engine for Natural Languages"** — K S Sunil et al., IEEE ICC 2023 (DOI: `10.1109/ICCC57789.2023.10165200`). Introduces the ALL framework: a tranSMachine with tranScripter and transCompiler components. This project is a direct implementation and extension of that paper's concepts.

2. **"Programming with Natural Languages: A Survey"** — Thomas J, Suresh V, Anas M, Sajeev S, Sunil K. In *Computer Networks and Inventive Communication Technologies* (Springer, 2021), pp. 767–779. DOI: `10.1007/978-981-16-3728-5_57`. The natural language survey that motivates the approach.

The project also extends the original [VishnuSuresh2000/JAVS-tranScripter](https://github.com/VishnuSuresh2000/JAVS-tranScripter) with:
- Full arithmetic support (power, modulo, comparison operators, increment/decrement)
- Fixed operand ordering in non-commutative operations
- Comprehensive test suite
- CI/CD pipeline

## How to Run

```bash
# Install dependencies
pip install nltk numpy

# Download NLTK data
python -c "import nltk; nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger')"

# Run a .ai file
python javs.py main.ai

# Generate Python code without executing
python javs.py main.ai -p

# Show transpilation log
python javs.py main.ai -l

# List registered Environment words
python javs.py -envWords
```

## Tests

```bash
# Unit tests
python test_arithmetic_env.py

# End-to-end tests
python test_e2e.py test_full.ai
```

## Documentation

- `Document/README_RESEARCH.md` — Research context and presentations
- `Document/presentation-all-nov-2020.md` — Original ALL concept presentation
- `Document/presentation-javs-working-apr-2021.md` — Implementation update presentation
- `ADR.md` — Architecture Decision Records
- LLM Wiki: [[JAVS-tranScripter]], [[Artificial Level Language (ALL) Paper]]