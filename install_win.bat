@echo off
echo === Installing dependencies (Windows) ===

IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

echo Instalando dependencias...
IF NOT EXIST requirements.txt (
    echo [ERROR] requirements.txt not found!
    exit /b 1
)
pip install -r requirements.txt
