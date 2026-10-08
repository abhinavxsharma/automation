import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    pg.wait_for_timeout(1000)
    btn = pg.get_by_role("button", name="Save progress & exit")
    if btn.count() > 0:
        print("Clicking 'Save progress & exit'...")
        btn.first.click()
        pg.wait_for_timeout(4000)
        pg.screenshot(path="scratch/after_save_progress_and_exit.png")
        print("Current URL:", pg.url)
        txt = pg.evaluate("() => document.body ? document.body.innerText : ''")
        print("Page preview:\n", txt[:400])
    else:
        # Try finding by text
        clicked = pg.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const b = btns.find(x => x.innerText && x.innerText.includes('Save progress & exit'));
            if (b) {
                b.click();
                return true;
            }
            return false;
        }""")
        print("JS click result:", clicked)
        pg.wait_for_timeout(4000)
        pg.screenshot(path="scratch/after_save_progress_and_exit.png")
        print("Current URL:", pg.url)
