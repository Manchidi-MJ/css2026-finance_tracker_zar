@echo off
echo Setting up FinTrack SA on Windows...
echo.

echo Step 1: Creating virtual environment...
python -m venv venv

echo Step 2: Activating virtual environment...
call venv\Scripts\activate

echo Step 3: Installing dependencies...
pip install --upgrade pip
pip install streamlit pandas numpy plotly

echo Step 4: Creating requirements.txt...
echo streamlit>=1.28.0 > requirements.txt
echo pandas>=2.0.0 >> requirements.txt
echo numpy>=1.24.0 >> requirements.txt
echo plotly>=5.0.0 >> requirements.txt

echo.
echo Setup complete!
echo To run the application:
echo 1. venv\Scripts\activate
echo 2. streamlit run finance_tracker_zar.py
pause