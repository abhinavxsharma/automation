import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    print("Waiting for page readiness...")
    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(1000)

    # Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0:
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(500)

    # Click Submit task button
    print("Clicking Submit task button...")
    submitted = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const sub = btns.find(b => b.innerText.trim() === 'Submit task' && b.offsetParent !== null);
        if (sub) {
            sub.click();
            return { success: true };
        }
        return { error: "Submit task button not found" };
    }""")
    print("Submit task clicked:", submitted)
    page.wait_for_timeout(2000)

    # Check for confirmation modal (e.g. Confirm, Yes, Submit anyway, etc.)
    confirm_info = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label')
        }));
        const dialog = document.querySelector('div[role="dialog"], div[class*="modal"], div[class*="z-50"]');
        return {
            dialogText: dialog ? dialog.innerText : null,
            buttons: btns
        };
    }""")
    print("Post-click dialog info:\n", confirm_info)

    # If confirmation dialog appears with a confirm/submit button, click it!
    if confirm_info.get("dialogText"):
        print("Confirmation dialog detected. Checking confirm buttons...")
        page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('div[role="dialog"] button, div[class*="z-50"] button'));
            const confirmBtn = btns.find(b => {
                const t = b.innerText.trim().toLowerCase();
                return t === 'submit' || t === 'confirm' || t === 'yes' || t === 'submit task';
            });
            if (confirmBtn) confirmBtn.click();
        }""")
        page.wait_for_timeout(3000)

    page.screenshot(path="scratch/after_submit_task.png")
    print("Saved screenshot to scratch/after_submit_task.png")

    print("Final URL:", page.url)
    print("Final title:", page.title())
