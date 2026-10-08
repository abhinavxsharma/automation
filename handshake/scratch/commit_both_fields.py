import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # 1. Dismiss timer modal
    btn = page.locator("button:has-text('Start timer')").first
    if btn.is_visible():
        box = btn.bounding_box()
        if box:
            print("Clicking Start timer at:", box)
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Click the black arrow button next to Cancel (for Science Judge justification)
    clicked = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel' && b.offsetParent !== null);
        if (!cancelBtn) return { error: "No visible Cancel button" };

        const parent = cancelBtn.parentElement;
        const buttons = Array.from(parent.querySelectorAll('button')).filter(b => b.offsetParent !== null);
        const arrowBtn = buttons.find(b => b !== cancelBtn);

        if (arrowBtn) {
            const rect = arrowBtn.getBoundingClientRect();
            arrowBtn.click();
            return { success: true, rect };
        }
        return { error: "No arrow button next to Cancel", buttons: buttons.map(b => b.innerText) };
    }""")
    print("Clicked justification submit button:", clicked)
    page.wait_for_timeout(2000)

    # 3. Click top Save button
    top_save = page.locator("button:has-text('Save')").first
    if top_save.is_visible():
        print("Clicking top Save button...")
        top_save.click(force=True)
        page.wait_for_timeout(2000)

    # 4. Screenshot and verify text
    page.screenshot(path="scratch/after_commit_both.png")
    txt = page.evaluate("() => document.body ? document.body.innerText : ''")
    Path("scratch/after_commit_text.txt").write_text(txt, encoding="utf-8")
    print("Saved scratch/after_commit_both.png and scratch/after_commit_text.txt")
