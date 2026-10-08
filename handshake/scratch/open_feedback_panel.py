import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # Click Feedback button in top nav if sidebar is collapsed
    fb_btn = page.locator("button[aria-label='Feedback']").first
    if fb_btn.count() > 0 and fb_btn.is_visible():
        print("Clicking Feedback button to open panel...")
        fb_btn.click()
        page.wait_for_timeout(1000)

    page.screenshot(path="handshake/scratch/feedback_panel_open.png")
    
    # Inspect all text in right half
    info = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('div, section, aside')).filter(el => {
            const rect = el.getBoundingClientRect();
            return rect.x > 800 && rect.width > 150 && rect.height > 200;
        });
        return els.map(el => el.innerText.trim()).filter(Boolean).slice(0, 3);
    }""")
    print("Right pane text:\n", info)
