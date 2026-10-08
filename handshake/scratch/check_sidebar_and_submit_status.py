import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Dismiss timer if visible
    btn = page.locator("button:has-text('Start timer')").first
    if btn.is_visible():
        box = btn.bounding_box()
        if box:
            print("Dismissing Start timer...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # Check if sidebar is open
    isOpen = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('*')).some(e => e.innerText && e.innerText.trim() === 'Feedback' && e.offsetWidth > 0);
    }""")
    print("Is sidebar open:", isOpen)

    if not isOpen:
        print("Opening sidebar...")
        fb_btn = page.locator("button[aria-label='Feedback']").first
        if fb_btn.is_visible():
            fb_btn.click()
            page.wait_for_timeout(1500)

    # Now read full state
    state = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const bannerLine = bodyText.split('\\n').find(l => l.includes('sent back') || l.includes('Distractor'));
        
        let sidebarText = '';
        const fbIdx = bodyText.indexOf('Feedback');
        if (fbIdx !== -1) {
            sidebarText = bodyText.slice(fbIdx, fbIdx + 800);
        }

        const subBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');

        return {
            bannerLine,
            sidebarText,
            subBtn: subBtn ? {
                text: subBtn.innerText.trim(),
                disabled: subBtn.disabled,
                classes: subBtn.className
            } : null,
            nextBtn: nextBtn ? {
                text: nextBtn.innerText.trim(),
                disabled: nextBtn.disabled
            } : null
        };
    }""")

    print("FULL STATE:\n", json.dumps(state, indent=2))
    page.screenshot(path="scratch/live_state_checked.png")
    print("Saved scratch/live_state_checked.png")
