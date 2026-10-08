import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=500):
        st_btn.click(force=True)
        page.wait_for_timeout(500)

    # Scroll window to bottom
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1000)

    # Also try scrolling document.documentElement
    page.evaluate("() => { if (document.scrollingElement) document.scrollingElement.scrollTop = document.scrollingElement.scrollHeight; }")
    page.wait_for_timeout(1000)

    page.screenshot(path="scratch/after_scroll_down.png")

    # Get all text
    body_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    print(f"Total body text length: {len(body_text)}")

    # Check Block 1
    if "Block 1" in body_text:
        idx1 = body_text.find("Block 1")
        print("\n=== BLOCK 1 SECTION ===")
        print(body_text[idx1:idx1+1500])

    # Check Block 2
    if "Block 2" in body_text:
        idx2 = body_text.find("Block 2")
        print("\n=== BLOCK 2 SECTION ===")
        print(body_text[idx2:idx2+1500])

    # Check Final Answer
    if "Final Answer" in body_text:
        idx_fa = body_text.find("Final Answer")
        print("\n=== FINAL ANSWER SECTION ===")
        print(body_text[idx_fa:idx_fa+500])
