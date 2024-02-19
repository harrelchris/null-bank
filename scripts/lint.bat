@echo off

call .venv\Scripts\activate

python -m black app

python -m flake8 app

python -m isort .
