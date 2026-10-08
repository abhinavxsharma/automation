import socket
import subprocess
import time
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE = str(Path.home() / ".handshake_chrome_profile")
TASK_URL = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"
PORT = 9222
DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200


def ensure_chrome():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        if s.connect_ex(("127.0.0.1", PORT)) == 0:
            return

    print("Launching independent Chrome on port 9222...")
    subprocess.Popen([
        CHROME,
        f"--remote-debugging-port={PORT}",
        f"--user-data-dir={PROFILE}",
        "--no-first-run",
        "--restore-last-session",
        TASK_URL
    ], creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP, close_fds=True)

    for i in range(30):
        time.sleep(0.5)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex(("127.0.0.1", PORT)) == 0:
                print(f"Chrome ready after {(i + 1) * 0.5}s")
                return
    raise RuntimeError("Chrome failed to open port 9222")


def get_task_page(playwright):
    ensure_chrome()
    browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "1520c7f4" in pg.url), None)
    if not page:
        page = next((pg for pg in browser.contexts[0].pages if "/task/" in pg.url), None)
    if not page:
        page = browser.contexts[0].pages[0]
    return browser, page

