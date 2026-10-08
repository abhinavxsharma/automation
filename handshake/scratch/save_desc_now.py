import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # 1. Dismiss timer modal
    # Try clicking the "Start timer" button
    print("Clicking Start timer...")
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible():
        st_btn.click(force=True)
        page.wait_for_timeout(1000)

    # If modal still open, press Escape
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 2. Now find the black arrow-up button next to Cancel
    arrow_info = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button" };

        const parent = cancelBtn.parentElement;
        const buttons = Array.from(parent.querySelectorAll('button'));
        const arrowBtn = buttons.find(b => b !== cancelBtn);

        if (arrowBtn) {
            const rect = arrowBtn.getBoundingClientRect();
            arrowBtn.click();
            return { success: true, rect };
        }
        return { error: "No arrow button next to Cancel", buttons: buttons.map(b => b.innerText) };
    }""")
    print("Clicked arrow button:", arrow_info)
    page.wait_for_timeout(2000)

    # Also click the top "Save" button to ensure everything is saved to server
    top_save = page.locator("button:has-text('Save')").first
    if top_save.is_visible():
        print("Clicking top Save button...")
        top_save.click(force=True)
        page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_desc_save_confirmed.png")
    print("Saved screenshot to scratch/after_desc_save_confirmed.png")
