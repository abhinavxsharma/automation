@echo off
title CrowdGen Maven Continuous Runner (Auto-Restart Mode)
echo ========================================================
echo Starting CrowdGen Maven Automation with Infinite Auto-Restart
echo To stop automation completely, press Ctrl+C
echo ========================================================

:restart_loop
echo [%date% %time%] Launching CrowdGen worker instance...
uv run python main.py

echo.
echo [%date% %time%] Worker process exited (code: %ERRORLEVEL%).
echo Auto-restarting in 5 seconds... (Press Ctrl+C to abort)
timeout /t 5 /nobreak >nul
goto restart_loop
