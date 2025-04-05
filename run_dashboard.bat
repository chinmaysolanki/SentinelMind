@echo off
echo Starting Cyber Brain Dashboard...
echo.
echo The dashboard will open in your default web browser automatically.
echo.
echo If it doesn't open automatically, please manually open:
echo http://localhost:8000
echo.
echo Press Ctrl+C to stop the server when you're done.
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
        echo Starting server...
        
        REM Start the server in the background
        start /B cmd /c "%%p simple_server.py"
        
        REM Wait a moment for the server to start
        timeout /t 2 /nobreak > nul
        
        REM Open the browser
        start http://localhost:8000
        
        echo.
        echo Server is running. Press Ctrl+C to stop.
        pause
        goto :end
    )
)

echo Python not found in common locations.
echo Please install Python 3.11 from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause

:end 