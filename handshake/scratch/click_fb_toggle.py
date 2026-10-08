import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(2000)
    
    # Click the feedback toggle button
    res = page.evaluate("""() => {
        // Find button around x=867, y=30
        const el = document.elementFromPoint(867, 30);
        if (el) {
            const btn = el.closest('button');
            if (btn) {
                btn.click();
                return 'Clicked ' + btn.outerHTML;
            }
            el.click();
            return 'Clicked el ' + el.outerHTML;
        }
        return 'No element at 867, 30';
    }""")
    print("Click result:", res)
    page.wait_for_timeout(2000)
    page.screenshot(path="scratch/after_toggle_fb.png")
