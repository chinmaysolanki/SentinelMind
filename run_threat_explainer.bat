@echo off
echo Running Cyber Threat Action Explainer...
echo.
echo This script will explain why specific actions were taken in response to cyber threats.
echo.

REM Try to find Python in common installation locations
set PYTHON_PATHS=^
C:\Python311\python.exe^
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe^
C:\Program Files\Python311\python.exe^
C:\Program Files (x86)\Python311\python.exe^
python.exe

for %%p in (%PYTHON_PATHS%) do (
    if exist %%p (
        echo Found Python at: %%p
        echo.
        echo Installing required packages...
        %%p -m pip install -r requirements.txt
        
        echo.
        echo Running threat explainer...
        %%p threat_explainer.py
        
        goto :end
    )
)

echo Python not found in common locations.
echo Please install Python 3.11 from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause

:end 