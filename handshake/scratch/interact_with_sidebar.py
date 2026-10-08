import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer if visible
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        b = st.bounding_box()
        if b:
            page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
            page.wait_for_timeout(1000)

    # 1. Click Feedback button in header
    fb_btn = page.locator("button[aria-label='Feedback']").first
    print("Clicking Feedback toggle...")
    fb_btn.click()
    page.wait_for_timeout(1500)

    # 2. Inspect sidebar
    sb_data = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const counter = bodyText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');

        // Look for buttons with circle-slash or inside the card
        const sjCard = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.includes('Science Judge - Lumiere') && e.children.length > 2);
        let cardButtons = [];
        if (sjCard) {
            cardButtons = Array.from(sjCard.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                title: b.getAttribute('title'),
                html: b.outerHTML.substring(0, 100),
                rect: b.getBoundingClientRect()
            }));
        }

        return {
            counter: counter ? counter[0] : null,
            nextBtn: nextBtn ? {
                text: nextBtn.innerText.trim(),
                disabled: nextBtn.disabled,
                rect: nextBtn.getBoundingClientRect()
            } : null,
            submitBtn: submitBtn ? {
                text: submitBtn.innerText.trim(),
                disabled: submitBtn.disabled
            } : null,
            cardButtons
        };
    }""")
    print("Sidebar data:\n", json.dumps(sb_data, indent=2))

    page.screenshot(path="scratch/sidebar_opened_live.png")
    print("Saved scratch/sidebar_opened_live.png")
