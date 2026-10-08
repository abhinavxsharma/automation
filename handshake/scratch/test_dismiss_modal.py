import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

def dismiss_timer_modal(page):
    print("Waiting for page / checking timer modal...")
    for _ in range(10):
        res = page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const st = btns.find(b => b.innerText && b.innerText.includes('Start timer'));
            if (st) {
                st.click();
                return { clicked: true };
            }
            return { clicked: false };
        }""")
        if res.get("clicked"):
            print("Successfully clicked 'Start timer' button!")
            page.wait_for_timeout(1500)
            return True
        page.wait_for_timeout(500)
    print("No 'Start timer' button found after waiting.")
    return False

with sync_playwright() as p:
    b, page = get_task_page(p)
    dismiss_timer_modal(page)
    page.screenshot(path="scratch/after_modal_dismissed_verified.png")
