"""End-to-end runner: transpile .ai files and execute the generated Python.

Usage:
    python test_e2e.py            # runs all *.ai files in this directory
    python test_e2e.py file.ai   # runs a single file
"""
import sys, os, subprocess, glob, traceback

REPO = os.path.dirname(os.path.abspath(__file__))
VENV_PY = os.path.join(REPO, '..', 'javs-venv', 'bin', 'python')
if not os.path.exists(VENV_PY):
    VENV_PY = sys.executable  # fallback to current interpreter


def run_e2e(ai_file):
    """Transpile and execute a .ai file. Returns (ok, stdout, stderr)."""
    proc = subprocess.run(
        [VENV_PY, os.path.join(REPO, 'javs.py'), ai_file],
        capture_output=True, text=True, cwd=REPO
    )
    return proc.returncode == 0, proc.stdout, proc.stderr


def main():
    if len(sys.argv) > 1:
        files = [f for f in sys.argv[1:] if f.endswith('.ai')]
    else:
        files = sorted(glob.glob(os.path.join(REPO, '*.ai')))

    if not files:
        print('No .ai files found')
        return 1

    failures = 0
    for f in files:
        try:
            ok, out, err = run_e2e(f)
            if ok:
                print(f'✓ {os.path.basename(f)}')
                if out.strip():
                    for line in out.strip().splitlines():
                        print(f'  {line}')
            else:
                failures += 1
                print(f'✗ {os.path.basename(f)}')
                print(f'  stderr: {err.strip()}')
        except Exception:
            failures += 1
            print(f'✗ {os.path.basename(f)}')
            traceback.print_exc()

    print(f'\n{failures} failures out of {len(files)} files')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())