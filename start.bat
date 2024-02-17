@echo off

:: Check for Python and provide installation link if not found
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed.
    echo Please install Python from https://www.python.org/downloads/
    exit /b
)

:: Assuming the script is run from the project directory

:: Activate the virtual environment
CALL venv\Scripts\activate.bat

:: Navigate to src directory
cd src

:: Install dependencies from requirements.txt
echo Installing dependencies...
pip install -r requirements.txt

:: Start the bot
echo Starting the bot...
python main.py

:: Navigate back to the project directory
cd ..

:: Deactivate the virtual environment
CALL venv\Scripts\deactivate.bat

pause

