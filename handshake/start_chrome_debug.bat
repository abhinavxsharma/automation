@echo off
set "CHROME_EXE=C:\Program Files\Google\Chrome\Application\chrome.exe"
if not exist "%CHROME_EXE%" (
    if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
        set "CHROME_EXE=C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ) else (
        set "CHROME_EXE=%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
    )
)

set "DEBUG_DIR=%USERPROFILE%\.handshake_chrome_profile"
echo Launching Google Chrome in Remote Debugging Mode on port 9222...
start "" "%CHROME_EXE%" --remote-debugging-port=9222 --user-data-dir="%DEBUG_DIR%" "https://ai.joinhandshake.com/fellow/15f2e875-62ac-492c-9e96-d5569635671a/tasks"
ping 127.0.0.1 -n 3 >nul
echo Chrome is now running on port 9222!
