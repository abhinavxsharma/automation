import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer modal via bounding box click
    st_btn = page.locator("button:has-text('Start timer')").first
    box = st_btn.bounding_box()
    if box:
        print("Dismissing Start timer modal via bounding box:", box)
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.wait_for_timeout(1000)

    # Now let's inspect the currently active textarea and surrounding buttons
    status = page.evaluate("""() => {
        const ta = document.querySelector('textarea');
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        
        let upBtnRect = null;
        if (cancelBtn && cancelBtn.parentElement) {
            const btns = Array.from(cancelBtn.parentElement.querySelectorAll('button'));
            const arrowBtn = btns.find(b => b !== cancelBtn);
            if (arrowBtn) {
                upBtnRect = arrowBtn.getBoundingClientRect();
            }
        }

        return {
            hasTextarea: !!ta,
            taValueSnippet: ta ? ta.value.substring(0, 100) : null,
            taRect: ta ? ta.getBoundingClientRect() : null,
            hasCancel: !!cancelBtn,
            cancelRect: cancelBtn ? cancelBtn.getBoundingClientRect() : null,
            upBtnRect
        };
    }""")
    print("Page status:", status)

    # If the up arrow button is present, click it!
    if status.get("upBtnRect"):
        r = status["upBtnRect"]
        cx = r["x"] + r["width"] / 2
        cy = r["y"] + r["height"] / 2
        print(f"Clicking submit arrow button at ({cx}, {cy})...")
        page.mouse.click(cx, cy)
        page.wait_for_timeout(2000)

    # Click top Save button
    top_save = page.locator("button:has-text('Save')").first
    if top_save.is_visible():
        print("Clicking top Save button...")
        top_save.click(force=True)
        page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_submit_step.png")
    txt = page.evaluate("() => document.body ? document.body.innerText : ''")
    Path("scratch/after_submit_text.txt").write_text(txt, encoding="utf-8")
    print("Saved scratch/after_submit_step.png and text.")
