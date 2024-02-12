@echo off
echo Starting PrionJoggo...
REM Activate virtual environment (if using one)
REM .\venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Run the bot
python src/bot.py

echo.
echo PrionJoggo has stopped.
pause

