import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    res = page.evaluate("""() => {
        const r = document.querySelector('input[type="radio"]');
        if (!r) return 'No radio';
        const key = Object.keys(r).find(k => k.startsWith('__reactFiber'));
        let cur = r[key];
        while (cur) {
            if (cur.memoizedProps && cur.memoizedProps.config && cur.memoizedProps.onChange) {
                cur.memoizedProps.onChange("label_element_misbinding");
                return 'Successfully set onChange to label_element_misbinding!';
            }
            cur = cur.return;
        }
        return 'Could not find onChange';
    }""")
    print("Result:", res)
    time.sleep(1)

    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(2)

    page.screenshot(path="scratch/after_correct_error_type.png")
    print("Screenshot saved to scratch/after_correct_error_type.png")
