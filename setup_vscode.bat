@echo off
echo Setting up FinTrack SA in Visual Studio...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate
echo Activating virtual environment...
call venv\Scripts\activate

REM Install packages with binary-only to avoid compilation
echo Installing packages...
pip install --upgrade pip
pip install streamlit pandas numpy plotly --only-binary=:all:

REM Create requirements.txt
echo streamlit==1.28.0 > requirements.txt
echo pandas==2.1.4 >> requirements.txt
echo numpy==1.26.0 >> requirements.txt
echo plotly==5.18.0 >> requirements.txt

echo.
echo Setup complete!
echo To run: streamlit run finance_tracker_zar.py
pause