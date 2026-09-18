# Environment-Based Learning Principles

## Core Idea

Natural language understanding and robot learning both require **procedural representation** — knowledge encoded as executable procedures that can call, modify, and extend themselves based on environmental feedback.

## Origin: SHRDLU (Winograd, 1971)

Terry Winograd's SHRDLU demonstrated a self-referential learning loop:

```
Command → Parser → Action Plan → Execute → World State Change
                                              ↓
                            Heuristic Understander
                                              ↓
                            Update Knowledge Procedures
                                              ↓
                            Self-discussion & reasoning
```

The robot learned from its own actions in a **blocks world** — not from external rewards, but from intrinsic feedback of success/failure.

## Key Principles

### 1. Procedural Representation
- Knowledge = executable procedures, not static rules
- Each concept (object property, grammar rule) becomes a callable program
- Enables recursion: procedures can modify other procedures
- Self-referential: the system can discuss its own reasoning

### 2. Self-Reinforcement Loop
- Agent executes actions → observes environmental feedback
- Success reinforces procedure; failure triggers modification
- No external reward signal — learning is intrinsic
- The loop: **act → observe → update → act again**

### 3. Micro-World Constraint
- Constrained environment (blocks world) enables focused learning
- All vocabulary known upfront
- Physics simplified (no gravity simulation)
- World state fully observable

### 4. Natural Language Interface
- English commands parse to executable procedures
- Questions query the world model
- System can explain its own actions
- Can request clarification when ambiguous

## Application to Ruto's tranScripter

Ruto's tranScripter applies these principles to programming language understanding:

| SHRDLU | Ruto's tranScripter |
|--------|-------------------|
| Blocks world | Programming environment |
| Robot arm commands | Python code generation |
| Natural English | Natural language instructions |
| World state database | ArithmeticEnv variables |
| Self-referential reasoning | RightHandTree parsing |

### Current Architecture

```
Natural Language Input
        ↓
    RightHandTree Parser
        ↓
    Environment Functions (store/add/print)
        ↓
    Python Code Generation
        ↓
    Execution & Feedback
```

### Environment Functions

The current `ArithmeticEnv` supports:
- `store X in $var` — variable assignment
- `add/subtract/multiply/divide` — arithmetic operations
- `print` — output results

### Learning Path Forward

Based on SHRDLU's principles, future development should add:

1. **Procedural Knowledge** — represent language constructs as callable functions
2. **Self-Modification** — allow the parser to update its own rules based on errors
3. **Expanded World Model** — more environment types beyond arithmetic
4. **Clarification Interface** — ask user when input is ambiguous
5. **Meta-Cognition** — ability to explain why a particular translation was chosen

## References

- [[Winograd SHRDLU]] — First demonstration of procedural representation in NLU
- [[Artificial Level Language (ALL) Paper]] — IEEE paper proposing ALL framework
- [[Ruto's tranScripter]] — Current implementation status

## See Also

- [[procedural-representation]]
- [[self-reinforcement-learning]]
- [[blocks-world]]