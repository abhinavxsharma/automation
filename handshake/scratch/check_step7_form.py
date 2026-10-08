import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("text=Project Lumière", timeout=15000)

    # Dismiss timer modal via JS
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # Click Edit on Step 7 via JS
    opened = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Edit this step']\"));
        if (btns[7]) {
            btns[7].scrollIntoView({ behavior: 'instant', block: 'center' });
            btns[7].click();
            return true;
        }
        return false;
    }""")
    print("Clicked Edit Step 7:", opened)
    page.wait_for_timeout(1500)

    # Inspect the form/card and submit button
    details = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: 'No cancel button found' };
        
        const card = cancelBtn.closest('[data-block-id]') || cancelBtn.closest('.border') || cancelBtn.parentElement;
        const submitBtn = cancelBtn.parentElement.querySelector(\"button[aria-label='Submit']\");
        
        // Find form or onSubmit
        const form = cancelBtn.closest('form');
        
        return {
            cardHTML: card ? card.innerHTML.slice(0, 1000) : null,
            formAction: form ? form.action : null,
            hasSubmitBtn: !!submitBtn,
            submitBtnDisabled: submitBtn ? submitBtn.disabled : null
        };
    }""")
    print("Step 7 form details:\n", details)

    # Cancel editor to leave page clean
    cancelled = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (cancelBtn) {
            cancelBtn.click();
            return true;
        }
        return false;
    }""")
    print("Cancelled editor:", cancelled)
