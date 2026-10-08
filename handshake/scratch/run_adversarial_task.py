"""Complete adversarial task execution script for Handshake AI.

Generates a new adversarial diagram, fills the task form, and runs
through all steps. Chrome must NOT be running before this script.
"""
import sys

sys.path.insert(0, ".")
import socket
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from handshake_automation.tasks.cs_diagram_creator import create_network_flow_diagram
from handshake_automation.tasks.problem_solver import solve_network_flow_task

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROFILE = str(Path.home() / ".handshake_chrome_profile")
TASK_URL = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"
PORT = 9222


def port_open():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(("127.0.0.1", PORT)) == 0
    except OSError:
        return False


def launch_chrome():
    cmd = [CHROME, f"--remote-debugging-port={PORT}",
           f"--user-data-dir={PROFILE}", "--no-first-run",
           "--restore-last-session", TASK_URL]
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for i in range(30):
        if port_open():
            print(f"Chrome ready after {i * 0.5}s")
            return
        time.sleep(0.5)
    print("Chrome port never opened!")
    sys.exit(1)


def dismiss_modals(page):
    """Dismiss any popups/modals that appear."""
    for sel in ['button:has-text("Got it")', 'button:has-text("Start timer")',
                'button:has-text("OK")', 'button:has-text("Dismiss")']:
        btn = page.locator(sel).first
        if btn.is_visible(timeout=2000):
            btn.click(force=True)
            page.wait_for_timeout(1000)
            print(f"  Dismissed: {sel}")


def click_continue(page):
    """Click the Continue/Next button."""
    for sel in ['button:has-text("Continue")', 'button:has-text("Next")']:
        btn = page.locator(sel).first
        if btn.is_visible(timeout=3000):
            btn.click(force=True)
            page.wait_for_timeout(2000)
            return True
    return False


def step_screenshot(page, name):
    page.screenshot(path=f"scratch/{name}.png")
    print(f"  Screenshot: scratch/{name}.png")


def main():
    # 1. Generate adversarial diagram + solve
    print("=== Step 0: Generate adversarial diagram ===")
    diagram_path = Path("scratch") / f"diagram_{int(time.time())}.png"
    info = create_network_flow_diagram(diagram_path)
    task_data = solve_network_flow_task(info)
    print(f"  Diagram: {diagram_path}")
    print(f"  GTFA: {task_data['gtfa']}")
    print(f"  Edges: {len(info['edges'])}")

    # 2. Launch Chrome
    print("\n=== Step 1: Launch Chrome ===")
    launch_chrome()
    time.sleep(5)

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        ctx = browser.contexts[0]
        page = next((pg for pg in ctx.pages if "/task/" in pg.url
                      and "71654a38" not in pg.url), ctx.pages[0])
        page.set_default_timeout(30000)
        print(f"  Connected to: {page.url}")
        page.wait_for_timeout(3000)

        # 3. Dismiss start timer modal
        print("\n=== Step 2: Dismiss modals ===")
        dismiss_modals(page)
        step_screenshot(page, "after_start_timer")

        # 4. Scroll to top and check current state
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(1000)
        step_screenshot(page, "task_state")

        print("\n=== Task is ready for manual form filling ===")
        print(f"GTFA: {task_data['gtfa']}")
        print(f"Diagram: {diagram_path.absolute()}")
        print(f"Prompt (first 150 chars): {task_data['prompt'][:150]}...")

        # Keep Chrome alive - don't close the browser connection
        print("\nChrome is connected. Press Ctrl+C to disconnect.")
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print("Disconnecting...")


if __name__ == "__main__":
    main()
