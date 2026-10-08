import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    res = page.evaluate("""() => {
        const input = document.querySelector('input[type="radio"][value="0"]');
        if (!input) return 'No input found';
        const key = Object.keys(input).find(k => k.startsWith('__reactFiber'));
        let fiber = input[key];
        
        let cur = fiber.return;
        while (cur) {
            if (cur.memoizedProps && cur.memoizedProps.onChange && cur.memoizedProps.config) {
                // This is the parent component E!
                const opt = cur.memoizedProps.config.options[0];
                const selected = [{ optionIndex: 0, value: opt.value, label: opt.label }];
                cur.memoizedProps.onChange(selected);
                return 'Called component.onChange with: ' + JSON.stringify(selected);
            }
            cur = cur.return;
        }
        return 'Did not find parent with config and onChange';
    }""")
    print("Result:", res)
    time.sleep(1)

    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(2)

    page.screenshot(path="scratch/after_parent_onchange.png")
    print("Screenshot saved to scratch/after_parent_onchange.png")
