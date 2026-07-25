@echo off
cd /d "%~dp0"
python run_lab.py
echo.
python -m unittest test_lab -v
