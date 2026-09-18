# 0003: E2E test runner as a generic subprocess wrapper

The project needed automated end-to-end testing: transpile a `.ai` file and execute the generated Python. We wrote `test_e2e.py` as a thin wrapper that invokes `javs.py` via `subprocess.run` on each `.ai` file. No per-environment scaffolding.

**Status:** accepted