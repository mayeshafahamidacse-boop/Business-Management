@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
    py -m venv .venv
    if errorlevel 1 goto :setup_failed
)
.venv\Scripts\python.exe -c "import flask, PIL, openpyxl" >nul 2>&1
if errorlevel 1 (
    .venv\Scripts\python.exe -m pip install "Flask>=3.0,<4" "Pillow>=10.0" "openpyxl>=3.1"
    if errorlevel 1 goto :setup_failed
)
.venv\Scripts\python.exe -m pip install "tzdata>=2024.1" >nul 2>&1
.venv\Scripts\python.exe run.py
pause
exit /b
:setup_failed
echo Could not prepare the Python environment. Check the error above and confirm internet access for package installation.
pause
