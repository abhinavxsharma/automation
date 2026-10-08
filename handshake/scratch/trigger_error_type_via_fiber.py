import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    res = page.evaluate("""() => {
        const r = document.querySelector('input[type="radio"][value="0"]');
        if (!r) return 'No radio';
        const key = Object.keys(r).find(k => k.startsWith('__reactFiber'));
        const fiber = r[key];
        
        // Find component with onChange
        let cur = fiber;
        let called = [];
        while (cur) {
            if (cur.memoizedProps && cur.memoizedProps.onChange) {
                try {
                    // Try calling onChange
                    if (cur.elementType && cur.elementType.name === 'E') {
                        cur.memoizedProps.onChange('0');
                        called.push('Called E.onChange("0")');
                    } else if (cur.elementType === 'input') {
                        cur.memoizedProps.onChange({ target: { value: '0', checked: true } });
                        called.push('Called input.onChange');
                    }
                } catch (e) {
                    called.push('Error: ' + e.message);
                }
            }
            cur = cur.return;
        }
        return called;
    }""")
    print("Trigger result:", res)
    time.sleep(1)

    # Now click Continue
    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(2)

    page.screenshot(path="scratch/after_fiber_trigger.png")
    print("Screenshot saved to scratch/after_fiber_trigger.png")
