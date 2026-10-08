import subprocess

ps = subprocess.run(
    ['powershell', '-NoProfile', '-Command', '(Get-CimInstance Win32_Process -Filter "Name = \'chrome.exe\'").CommandLine'],
    capture_output=True, text=True
)
for line in ps.stdout.splitlines():
    if line.strip():
        print(line[:120])
