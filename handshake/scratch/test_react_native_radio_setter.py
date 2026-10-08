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
        
        // Reset and use native prototype setter
        const proto = window.HTMLInputElement.prototype;
        const setChecked = Object.getOwnPropertyDescriptor(proto, 'checked').set;
        setChecked.call(input, true);
        
        input.dispatchEvent(new Event('click', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        input.dispatchEvent(new Event('input', { bubbles: true }));
        
        return 'Dispatched native click and change!';
    }""")
    print("Evaluate result:", res)
    time.sleep(1)

    page.screenshot(path="scratch/after_native_setter.png")
    print("Screenshot saved to scratch/after_native_setter.png")
