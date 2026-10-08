import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Click the radio button for Label-element or axis mis-binding
    page.evaluate("""() => {
        const labels = Array.from(document.querySelectorAll('label'));
        const target = labels.find(l => l.innerText && l.innerText.trim() === 'Label–element or axis mis-binding');
        if (target) {
            target.scrollIntoView({ block: 'center' });
            target.click();
            // Also click associated input
            const input = target.previousElementSibling;
            if (input && input.type === 'radio') {
                input.checked = true;
                input.dispatchEvent(new Event('change', { bubbles: true }));
                input.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    }""")
    time.sleep(1)

    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(2)

    page.screenshot(path="scratch/after_error_type_selected.png")
    print("Screenshot saved to scratch/after_error_type_selected.png")
