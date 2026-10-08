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

    for i in range(20):
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
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0]
        pages = ctx.pages
        print(f"Total open pages: {len(pages)}")
        for i, pg in enumerate(pages):
            print(f"  Page {i}: {pg.url}")

        page = next((pg for pg in pages if "/task/1520c7f4" in pg.url), None)
        if not page:
            page = next((pg for pg in pages if "/task/" in pg.url), pages[0])

        print(f"Active page: {page.url}")
        page.wait_for_timeout(2000)

        # Take full page screenshot
        page.screenshot(path="scratch/current_full_state.png", full_page=True)
        print("Saved full page screenshot to scratch/current_full_state.png")

        # Check prompt checker feedback
        feedback_el = page.locator("aside, div:has-text('Prompt Checker')").first
        if feedback_el.is_visible(timeout=2000):
            print("--- Prompt Checker Text ---")
            print(feedback_el.inner_text()[:1500])

        # Check form fields visible
        print("\n--- Current Form State ---")
        inputs = page.locator("input, textarea, select, [role='combobox']").all()
        for inp in inputs:
            try:
                vis = inp.is_visible()
                val = inp.input_value() if inp.evaluate("el => 'value' in el") else inp.inner_text()
                ph = inp.get_attribute("placeholder") or ""
                aria = inp.get_attribute("aria-label") or ""
                if vis:
                    print(f"  Input: ph='{ph}' aria='{aria}' val='{val[:60]}'")
            except Exception:
                pass


if __name__ == "__main__":
    main()
