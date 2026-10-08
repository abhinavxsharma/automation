import subprocess, os, time, urllib.request

chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
profile_dir = os.path.expanduser(r"~\.handshake_chrome_profile")
cmd = [
    chrome_exe,
    "--remote-debugging-port=9222",
    f"--user-data-dir={profile_dir}",
    "--no-first-run",
    "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"
]

print("Launching Chrome:", cmd)
proc = subprocess.Popen(cmd)
print("PID:", proc.pid)

time.sleep(3)
for attempt in range(10):
    try:
        resp = urllib.request.urlopen("http://127.0.0.1:9222/json/version", timeout=1)
        data = resp.read().decode()
        print("Success! Version info:", data)
        break
    except Exception as e:
        print(f"Attempt {attempt}: {e}")
        time.sleep(1)
