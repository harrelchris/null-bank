@echo off

call .venv\Scripts\activate

python -m black app --line-length 119 --exclude migrations/

python -m flake8 app

:: python -m isort . --profile black
