import socket
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE = str(Path.home() / ".handshake_chrome_profile")
TASK_URL = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"
PORT = 9222


def ensure_chrome():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        if s.connect_ex(("127.0.0.1", PORT)) == 0:
            print("Port 9222 already open.")
            return

    print("Launching Chrome on port 9222...")
    subprocess.Popen([
        CHROME,
        f"--remote-debugging-port={PORT}",
        f"--user-data-dir={PROFILE}",
        "--no-first-run",
        "--restore-last-session",
        TASK_URL
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for i in range(30):
        time.sleep(0.5)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex(("127.0.0.1", PORT)) == 0:
                print(f"Chrome ready after {(i + 1) * 0.5}s")
                return
    raise RuntimeError("Chrome failed to open port 9222")


def main():
    ensure_chrome()
    time.sleep(2)

    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        pg = next((t for t in b.contexts[0].pages if "/task/1520c7f4" in t.url), None)
        if not pg:
            pg = next((t for t in b.contexts[0].pages if "/task/" in t.url), b.contexts[0].pages[0])

        # Dismiss timer modal
        st_btn = pg.locator("button:has-text('Start timer')").first
        if st_btn.is_visible(timeout=3000):
            st_btn.click()
            pg.wait_for_timeout(1000)
            print("Clicked Start timer modal")

        # Let's inspect all text in the main scrollable area
        main_text = pg.evaluate("""() => {
            const main = document.querySelector('main') || document.body;
            return main.innerText;
        }""")
        with open("scratch/page_text.txt", "w", encoding="utf-8") as f:
            f.write(main_text)
        print("Wrote page text to scratch/page_text.txt")

        # Also capture screenshot of the current page after dismissing modal
        pg.screenshot(path="scratch/after_dismiss_timer.png")
        print("Screenshot saved to scratch/after_dismiss_timer.png")


if __name__ == "__main__":
    main()
