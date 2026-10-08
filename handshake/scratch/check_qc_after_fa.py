import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_timeout(10000)

    # Check sidebar
    side_text = page.evaluate("""() => {
        const side = document.querySelector("[data-testid='task-side-panel'], div.w-80");
        return side ? side.innerText.trim() : 'NO_SIDEBAR';
    }""")
    print("Sidebar status:\n", side_text)

    page.screenshot(path="handshake/scratch/qc_after_fa_check.png")
    print("Screenshot saved to handshake/scratch/qc_after_fa_check.png")
