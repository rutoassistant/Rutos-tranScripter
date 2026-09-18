# 0002: GitHub Actions CI with Alpine Linux containers

The project had no CI/CD. Tests existed but ran only locally. We use GitHub Actions with `python:3.12-alpine` containers — the `runs-on` host stays `ubuntu-latest` but every job step executes inside Alpine via the `container:` directive.

**Status:** accepted