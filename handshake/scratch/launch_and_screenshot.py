"""Launch Chrome with CDP, wait for port, connect, screenshot."""
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE = str(Path.home() / ".handshake_chrome_profile")
URL = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"
PORT = 9222

def port_open():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(("127.0.0.1", PORT)) == 0
    except OSError:
        return False

# Launch Chrome
cmd = [CHROME, f"--remote-debugging-port={PORT}", f"--user-data-dir={PROFILE}", "--no-first-run", "--restore-last-session", URL]
proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"Chrome PID: {proc.pid}")

# Wait for port
for i in range(30):
    if port_open():
        print(f"Port {PORT} open after {i*0.5}s")
        break
    time.sleep(0.5)
else:
    print("Port never opened!")
    sys.exit(1)

# Extra wait for page load
time.sleep(5)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    ctx = browser.contexts[0]
    pages = ctx.pages
    print(f"Pages: {[(pg.url, pg.title()) for pg in pages]}")
    # Find task page
    page = next((pg for pg in pages if "/task/" in pg.url and "71654a38" not in pg.url), pages[0])
    page.wait_for_timeout(3000)
    page.screenshot(path="scratch/current_screen.png")
    print(f"Screenshot saved. URL: {page.url}, Title: {page.title()}")
