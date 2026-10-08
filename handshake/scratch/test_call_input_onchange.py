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
        const fiber = input[key];
        
        if (fiber.memoizedProps && fiber.memoizedProps.onChange) {
            fiber.memoizedProps.onChange();
            return 'Called fiber.memoizedProps.onChange() successfully!';
        }
        return 'No onChange found on fiber';
    }""")
    print("Result:", res)
    time.sleep(1)

    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(2)

    page.screenshot(path="scratch/after_calling_fiber_input_onchange.png")
    print("Screenshot saved to scratch/after_calling_fiber_input_onchange.png")
