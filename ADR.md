# Architecture Decision Records

## ADR-001: ArithmeticEnv as the sole Environment implementation

**Status:** Accepted  
**Date:** 2026-09-18

### Context

The JAVS-tranScripter transpiler supports pluggable "Environments" — each Environment maps natural-language words to Python code generation functions. The original `arithmeticEnv.py` was the only environment and contained 12 built-in operations.

### Decision

Keep `arithmeticEnv.py` as the single Environment implementation. No new Environment classes until a second language domain is needed.

### Consequences

- **Pro:** Minimal surface area; one file to understand, test, and maintain.
- **Pro:** E2E runner (`test_e2e.py`) is environment-agnostic — it just runs `javs.py` on `.ai` files, so adding a second env requires no runner changes.
- **Con:** If a second env is added later, the runner will need per-env `.ai` test files. Add a per-env runner at that point.

---

## ADR-002: GitHub Actions CI with Alpine Linux containers

**Status:** Accepted  
**Date:** 2026-09-18

### Context

The project had no CI/CD pipeline. Tests existed (`test_arithmetic_env.py`, `test_e2e.py`) but ran only locally. The user wanted minimal-footprint runners.

### Decision

Use GitHub Actions with `python:3.12-alpine` containers. The `runs-on` host remains `ubuntu-latest` (GitHub has no native Alpine runner), but every job step executes inside the Alpine container via the `container:` directive.

### Consequences

- **Pro:** Tests run on musl-based minimal Linux, matching the user's preference for small-footprint runners.
- **Pro:** Single job definition, no duplicate ubuntu/alpine jobs.
- **Con:** `runs-on` still reports `ubuntu-latest` in the workflow UI — the Alpine execution is transparent but the label doesn't change. A self-hosted Alpine runner would change the label but requires manual provisioning.

---

## ADR-003: E2E test runner as a generic subprocess wrapper

**Status:** Accepted  
**Date:** 2026-09-18

### Context

The project needed automated end-to-end testing: transpile a `.ai` file and execute the generated Python. The user asked for a runner that works across environments.

### Decision

Write `test_e2e.py` as a thin wrapper that invokes `javs.py` via `subprocess.run` on each `.ai` file. No per-environment scaffolding.

### Consequences

- **Pro:** Works for any environment without code changes — it's env-agnostic by design.
- **Pro:** Usage is trivial: `python test_e2e.py [file.ai ...]`.
- **Con:** No per-environment runner scaffolding exists. Add one when a second Environment lands.

---

## ADR-004: Squash duplicate commits on arithmeticEnv fixes

**Status:** Accepted  
**Date:** 2026-09-18

### Context

Two commits with the same message ("Fix arithmetic operand order bugs in compare operations") were created during iterative debugging of `arithmeticEnv.py`. The first commit (`ea71fdf`) was incomplete; the second (`d76293e`) added the remaining fixes.

### Decision

Squash both into a single commit (`9a87cf5`) with a descriptive message covering all changes: added operations, fixed operand order in divide/subtract/power/modulo, and fixed lt/gt/le/ge.

### Consequences

- **Pro:** Clean git history — one commit per logical change.
- **Pro:** The squash preserved all file changes (arithmeticEnv.py + test_arithmetic_env.py + test_full.ai).