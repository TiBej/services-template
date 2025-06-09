```bash
cd first-service
uv sync
pyright . # successful

cd second-service
uv sync
pyright . # successful

cd common
uv sync
pyright . # reportMissingImports (separate issue, I think)
uv run pyright . # successful

# in root
pyright . # reportMissingImports
```

1. opening whole repository in VSC import errors I.e. in first-service/main.py
2. opening only first-service in VSC no import errors.
