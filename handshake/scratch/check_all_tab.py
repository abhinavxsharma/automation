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

    # Click All tab
    page.evaluate("""() => {
        const allBtns = Array.from(document.querySelectorAll('*')).filter(e => e.innerText && e.innerText.trim() === 'All');
        if (allBtns.length > 0) allBtns[allBtns.length - 1].click();
    }""")
    page.wait_for_timeout(1000)

    # Dismiss modal if present
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(500)

    sidebar_text = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const fbIdx = bodyText.indexOf('Feedback');
        return fbIdx !== -1 ? bodyText.slice(fbIdx, fbIdx + 600) : 'None';
    }""")
    print("All Tab Status:\n", sidebar_text)

    # Check Disagree buttons count in All tab
    btns = page.locator("button[aria-label='Disagree']").all()
    print("Disagree buttons count in All tab:", len(btns))

    page.screenshot(path="handshake/scratch/all_tab_check.png")
