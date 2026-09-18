# Ruto's transScripter

Research-based natural-language-to-Python transpiler. Accepts sentences in a controlled subset of English (`.ai` files) and compiles them into executable Python statements. Not production-grade — a research prototype.

## Language

**ArithmeticEnv**:
A pluggable Environment class that maps natural-language words to Python code generators. Currently the sole Environment. Contains 12 operations: add, subtract, multiply, divide, power, modulo, lt, gt, eq, ne, le, ge.

_Avoid_: Environment class, language module

**Environment**:
A class with `env_Words_and_WordAsFunction` dict mapping words → static methods that return Python code strings. Pluggable — multiple Environments can coexist.

_Avoid_: Context, domain, scope

**tranScripter**:
The parsing component of the ALL framework. Tokenizes natural language, builds a sentence tape, and dispatches to Environment functions.

_Avoid_: Parser, tokenizer, lexer

**transCompiler**:
The planned second component of the ALL framework. Would convert the tranScripter's output into a target language (Python, C, etc.).

_Avoid_: Code generator, compiler

**RightHandTree**:
The internal data structure that represents parsed sentence structure. Used by the machine to walk the tape.

_Avoid_: AST, parse tree, syntax tree

**Machine**:
The execution engine that walks the reversed sentence tape and dispatches to Environment functions.

_Avoid_: Interpreter, executor, VM

**Variable**:
A named storage location. Uses `$` prefix in `.ai` files (e.g. `$v1`), stripped in generated Python (`v1`).

_Avoid_: Symbol, register, memory cell

**String literal**:
A quoted string in `.ai` files. Uses `~` prefix (e.g. `~hello`), converted to `"hello"` in Python.

_Avoid_: Text literal, string constant

## Rules

- **Pluggable Environments**: Each Environment is a class with a dict mapping words → static methods. New domains require new Environment classes.
- **Tape reversal**: `machine.py` iterates `reversed(sentenceTape)`, so non-commutative operations must internally reverse their args.
- **`$` prefix**: Variables in `.ai` files use `$`. Generated Python strips it.
- **`~` prefix**: String literals in `.ai` files use `~`. Generated Python converts to `"..."`.
- **Controlled grammar**: Sentences must follow specific patterns. Out-of-pattern input fails or produces incorrect code.

## Research Foundations

- **"Artificial Level Language: A Library of Computing Engine for Natural Languages"** — K S Sunil et al., IEEE ICC 2023. Introduces the ALL framework: a tranSMachine with tranScripter and transCompiler.
- **"Programming with Natural Languages: A Survey"** — Thomas J, Suresh V, Anas M, Sajeev S, Sunil K. Springer, 2021. The natural language survey motivating the approach.
- **"Procedures as a Representation for Data in a Computer Program for Understanding Natural Language"** — Terry Winograd, MIT AI Lab, 1971. Introduces procedural representation and self-reinforcement learning in the SHRDLU blocks world.