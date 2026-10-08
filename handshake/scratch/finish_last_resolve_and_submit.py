import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

FINAL_REASON = (
    "Addressed by providing a detailed mathematical and structural justification in the Science Judge section "
    "proving that the critical path duration 76 ms is uniquely determined with zero ambiguity."
)

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    print("Waiting for page load...")
    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(1000)

    # Dismiss timer modal
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0:
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing Start timer...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 1. Click Resolve on the remaining item
    print("Clicking Resolve on remaining item...")
    r_btn = page.locator("button[aria-label='Resolve']").first
    if r_btn.is_visible():
        r_btn.click()
        page.wait_for_timeout(1000)

    # 2. Fill the resolve reason textarea
    ta = page.locator("textarea[placeholder*='resolve reason'], textarea[placeholder*='Reply']:visible").first
    if ta.count() > 0 and ta.is_visible():
        print("Filling final resolve reason...")
        ta.fill(FINAL_REASON)
        page.wait_for_timeout(500)

        # 3. Click the send airplane button
        print("Clicking send airplane button...")
        sent = page.evaluate("""() => {
            const ta = document.querySelector("textarea[placeholder*='resolve reason'], textarea[placeholder*='Reply']");
            if (!ta) return { error: "No textarea" };
            let p = ta.parentElement;
            while (p && p.tagName !== 'SECTION' && p !== document.body) {
                const btns = Array.from(p.querySelectorAll('button')).filter(b => {
                    const aria = b.getAttribute('aria-label') || '';
                    return b.querySelector('svg') && aria !== 'Resolve' && aria !== 'Disagree' && aria !== 'Close';
                });
                if (btns.length > 0) {
                    btns[0].click();
                    return { success: true };
                }
                p = p.parentElement;
            }
            return { error: "No send button found" };
        }""")
        print("Send result:", sent)
        page.wait_for_timeout(2000)

    # 4. Check addressed counter
    counter = page.evaluate("""() => {
        const body = document.body.innerText;
        const m = body.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        return m ? m[0] : 'Not found';
    }""")
    print("Counter now:", counter)

    # 5. Click top Save
    save_btn = page.locator("button:has-text('Save')").first
    if save_btn.is_visible():
        save_btn.click()
        page.wait_for_timeout(2000)

    # 6. Click Submit task
    print("Looking for Submit task button...")
    sub_res = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const sub = btns.find(b => b.innerText.trim() === 'Submit task');
        if (sub) {
            sub.click();
            return { success: true };
        }
        return { error: "Submit task not found", allButtons: btns.map(b => b.innerText.trim()).filter(Boolean) };
    }""")
    print("Submit task result:", sub_res)
    page.wait_for_timeout(3000)

    # Check for confirmation modal (e.g. Confirm, Yes, Submit anyway, etc.)
    confirm_res = page.evaluate("""() => {
        const dialog = document.querySelector('div[role="dialog"], div[class*="z-50"]');
        if (!dialog) return { hasDialog: false };
        const btns = Array.from(dialog.querySelectorAll('button'));
        const confirmBtn = btns.find(b => {
            const t = b.innerText.trim().toLowerCase();
            return t === 'submit' || t === 'confirm' || t === 'yes' || t === 'submit task';
        });
        if (confirmBtn) {
            confirmBtn.click();
            return { hasDialog: true, clicked: confirmBtn.innerText.trim() };
        }
        return { hasDialog: true, dialogText: dialog.innerText, buttons: btns.map(b => b.innerText.trim()) };
    }""")
    print("Confirmation modal result:", confirm_res)
    page.wait_for_timeout(3000)

    page.screenshot(path="scratch/final_submission_completed.png")
    print("Final screenshot saved to scratch/final_submission_completed.png")
    print("Final URL:", page.url)
