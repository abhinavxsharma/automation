import sys
import time

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # First, cancel the description editor if still open
    cancel_res = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (cancelBtn) {
            cancelBtn.click();
            return 'Cancelled open editor';
        }
        return 'No open editor';
    }""")
    print("Cancel result:", cancel_res)
    time.sleep(1)

    # Now find the Science Judge section edit button
    res = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const target = all.find(e => e.innerText && e.innerText.includes('Pay close attention to the Science Judge') && e.children.length === 0);
        if (!target) return { error: "Target heading not found" };

        let container = target;
        let editBtn = null;
        for (let i = 0; i < 10; i++) {
            if (!container) break;
            editBtn = container.querySelector('button[aria-label="Edit this step"]');
            if (editBtn) break;
            container = container.parentElement;
        }

        if (editBtn) {
            editBtn.scrollIntoView({ behavior: 'instant', block: 'center' });
            editBtn.click();
            return { success: true };
        }

        return { error: "Edit button not found near Science Judge" };
    }""")

    print("Click edit Science Judge result:", res)
    time.sleep(1)

    # Check if textarea appeared
    ta_count = page.locator("textarea").count()
    print(f"Textareas visible: {ta_count}")
    if ta_count > 0:
        ta_val = page.locator("textarea").first.input_value()
        print(f"Textarea current value: {ta_val!r}")

    page.screenshot(path="scratch/check_sj_editor_open.png")
