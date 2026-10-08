import subprocess

cmd = 'powershell "Get-Process chrome -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Id"'
pids = subprocess.check_output(cmd, shell=True).decode().split()
print("Found Chrome PIDs:", len(pids))

cmd_cl = 'powershell "Get-CimInstance Win32_Process -Filter \\\"name=\'chrome.exe\'\\\" | Select-Object CommandLine"'
cl_out = subprocess.check_output(cmd_cl, shell=True).decode()
has_port = False
for line in cl_out.splitlines():
    if "remote-debugging-port" in line:
        has_port = True
        print("Found line:", line[:120])
if not has_port:
    print("No remote-debugging-port found in running Chrome processes.")
