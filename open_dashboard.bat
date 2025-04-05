@echo off
echo Opening Cyber Brain Dashboard...
echo.
echo The dashboard will open in your default web browser.
echo.
echo If it doesn't open automatically, please manually open the file:
echo %~dp0standalone_dashboard.html
echo.
echo Press any key to continue...
pause > nul

start "" "%~dp0standalone_dashboard.html" 