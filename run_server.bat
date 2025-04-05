@echo off
echo Starting Cyber Brain Dashboard Server...
echo.
echo Please wait while the server starts...
echo.
echo Once started, open http://localhost:5000 in your web browser
echo.
echo Press Ctrl+C to stop the server
echo.

REM Try to find Python in common installation locations
set PYTHON_PATHS=^
C:\Python311\python.exe^
C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python311\python.exe^
C:\Program Files\Python311\python.exe^
C:\Program Files (x86)\Python311\python.exe

for %%p in (%PYTHON_PATHS%) do (
    if exist %%p (
        echo Found Python at: %%p
        echo Installing required packages...
        %%p -m pip install flask flask-cors
        echo.
        echo Starting server...
        %%p server.py
        goto :end
    )
)

echo Python not found in common locations.
echo Please install Python 3.11 from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause

:end 