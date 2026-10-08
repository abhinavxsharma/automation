@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo Starting Handshake AI Project Lumiere Automation
echo Autonomous Execution with Infinite Auto-Restart
echo Press Ctrl+C at any time to stop completely.
echo ========================================================

:LOOP
echo [%DATE% %TIME%] Launching Handshake worker...
uv run python main.py
set EXITCODE=%ERRORLEVEL%

if %EXITCODE% EQU 0 (
    echo [%DATE% %TIME%] Worker finished normally. Restarting in 5 seconds...
    timeout /t 5 /nobreak >nul
    goto LOOP
)

echo [%DATE% %TIME%] Worker crashed or exited with code %EXITCODE%.
echo [%DATE% %TIME%] Auto-recovering and restarting in 10 seconds...
timeout /t 10 /nobreak >nul
goto LOOP
