import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    inp = page.locator("input[placeholder='Start typing...'], input[type='text']").first
    inp.scroll_into_view_if_needed()
    time.sleep(0.5)
    print("Typing 76 into Final Answer...")
    inp.fill("76")
    page.wait_for_timeout(300)
    page.evaluate("""() => {
        const inp = document.querySelector("input[placeholder='Start typing...']") || document.querySelector("input[type='text']");
        if (inp) {
            inp.value = '76';
            inp.dispatchEvent(new Event('input', { bubbles: true }));
            inp.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""")
    time.sleep(0.5)

    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(2)

    page.screenshot(path="scratch/after_final_answer_continue.png")
    print("Screenshot saved to scratch/after_final_answer_continue.png")
