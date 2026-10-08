import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

TEST_TEXT = "Test description update without duplicate."

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Dismiss modal if open
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0:
        box = modal_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(500)

    # 1. Click edit on description
    page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const target = all.find(e => e.innerText && e.innerText.includes('minimum of 200 words') && e.children.length === 0);
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
        }
    }""")
    page.wait_for_timeout(1000)

    # 2. Inspect the textarea and commit button before change
    before_info = page.evaluate("""() => {
        const ta = document.querySelector('textarea');
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        const commitBtn = cancelBtn ? Array.from(cancelBtn.parentElement.querySelectorAll('button')).find(b => b !== cancelBtn) : null;
        return {
            taFound: !!ta,
            taValLength: ta ? ta.value.length : 0,
            commitBtnFound: !!commitBtn,
            commitBtnDisabled: commitBtn ? commitBtn.disabled : null,
            commitBtnAria: commitBtn ? commitBtn.getAttribute('aria-label') : null,
            commitBtnHtml: commitBtn ? commitBtn.outerHTML : null
        };
    }""")
    print("Before change:", before_info)

    # 3. Use Playwright locator.fill() which uses Chrome DevTools protocol to simulate real keyboard input and React state update!
    ta = page.locator("textarea").first
    print("Using Playwright fill()...")
    ta.fill("Clean test text 12345")
    page.wait_for_timeout(500)

    after_fill_info = page.evaluate("""() => {
        const ta = document.querySelector('textarea');
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        const commitBtn = cancelBtn ? Array.from(cancelBtn.parentElement.querySelectorAll('button')).find(b => b !== cancelBtn) : null;
        return {
            taVal: ta ? ta.value : '',
            commitBtnDisabled: commitBtn ? commitBtn.disabled : null
        };
    }""")
    print("After fill:", after_fill_info)

    # Cancel so we don't save the test text yet
    cancel_btn = page.locator("button:has-text('Cancel')").first
    if cancel_btn.is_visible():
        cancel_btn.click()
        print("Cancelled test.")
