@echo off
echo ========================================================
echo Starting Google Chrome in Remote Debugging Mode (Port 9222)
echo ========================================================

set "CHROME_EXE=C:\Program Files\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME_EXE%" (
    if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
        set "CHROME_EXE=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ) else (
        set "CHROME_EXE=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
    )
)

set "DEBUG_DIR=%USERPROFILE%\.chrome-debug"
echo Using persistent debug profile: %DEBUG_DIR%
echo Launching Google Chrome on port 9222...

start "" "%CHROME_EXE%" --remote-debugging-port=9222 --user-data-dir="%DEBUG_DIR%" https://dq0uw9vf3nt8l.cloudfront.net
timeout /t 2 /nobreak >nul

echo.
echo ========================================================
echo Chrome is now running on port 9222 with Maven opened!
echo Sign in if needed, open your task, and in terminal run:
echo   uv run python main.py
echo ========================================================
