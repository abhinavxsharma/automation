import subprocess, json

cmd = ["powershell", "-NoProfile", "-Command", "Get-Process chrome | Select-Object Id, MainWindowTitle | ConvertTo-Json"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Output:\n", res.stdout)
