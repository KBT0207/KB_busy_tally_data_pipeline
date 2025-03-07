@echo off
cd /d E:\automationProject\busy_tally_pipeline
call .venv\Scripts\activate.bat
poetry run python main.py
