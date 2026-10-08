import subprocess, os, time, sys

chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
profile_dir = os.path.expanduser(r"~\.handshake_chrome_profile")
cmd = [
    chrome_exe,
    "--remote-debugging-port=9222",
    f"--user-data-dir={profile_dir}",
    "--no-first-run",
    "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"
]

print("Starting Chrome keeper process...", flush=True)
proc = subprocess.Popen(cmd)
print(f"Chrome running with PID {proc.pid}", flush=True)

try:
    while True:
        if proc.poll() is not None:
            print("Chrome exited, restarting...", flush=True)
            proc = subprocess.Popen(cmd)
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping Chrome keeper...", flush=True)
    proc.terminate()
