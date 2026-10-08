import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save'), button:has-text('Start timer')", timeout=15000)
    page.wait_for_timeout(1000)

    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        st_btn.first.click()
        page.wait_for_timeout(1000)

    # Let's inspect the callout element and the submit button in the prompt card
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    prompt_btn = edit_btns[7]
    prompt_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    prompt_btn.click()
    page.wait_for_timeout(1000)

    info = page.evaluate("""() => {
        // Find the callout
        const callout = document.querySelector("div[class*='alert'], [role='alert'], div.border");
        // Find submit button in this card
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        const submitBtn = cancelBtn ? cancelBtn.parentElement.querySelector("button[aria-label='Submit']") : null;
        
        function getFiber(dom) {
            const key = Object.keys(dom || {}).find(k => k.startsWith('__reactFiber$'));
            return key ? dom[key] : null;
        }

        const fiber = getFiber(submitBtn);
        let current = fiber;
        let handlers = [];
        while (current && handlers.length < 5) {
            if (current.memoizedProps) {
                for (let k of Object.keys(current.memoizedProps)) {
                    if (k.startsWith('on') && typeof current.memoizedProps[k] === 'function') {
                        handlers.push({ prop: k, fn: current.memoizedProps[k].toString().substring(0, 200) });
                    }
                }
            }
            current = current.return;
        }

        return {
            calloutText: callout ? callout.innerText : null,
            submitBtnHTML: submitBtn ? submitBtn.outerHTML : null,
            handlers: handlers
        };
    }""")
    print("Callout and Handlers info:\n", info)

    # Cancel prompt editor
    cancel_btn = page.locator("button:has-text('Cancel')").first
    if cancel_btn.is_visible():
        cancel_btn.click()
        page.wait_for_timeout(1000)
