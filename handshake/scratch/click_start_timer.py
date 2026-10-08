import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.append(str(Path(__file__).parent))
from chrome_helper import get_task_page


def main():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        page.wait_for_selector("text=Computer Systems", timeout=15000)

        # Look for the Start timer button
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible(timeout=3000):
            print("Start timer button is visible, clicking it...")
            st.click()
            time.sleep(1.5)
        else:
            print("Start timer button not directly visible, checking top timer pill...")

        page.screenshot(path="handshake/scratch/after_start_timer.png")
        print("Saved after_start_timer.png")

        # Now check if modal is gone
        st2 = page.locator("button:has-text('Start timer')").first
        print("Modal still visible?", st2.is_visible())


if __name__ == "__main__":
    main()
