import sys
import time

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Wait for page hydration
    for _ in range(20):
        t = page.evaluate("() => document.body ? document.body.innerText : ''")
        if len(t) > 200:
            break
        time.sleep(0.5)

    print("Page hydrated. Body text length:", len(t))

    # Click Start timer if visible
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        print("Found Start timer button. Clicking it...")
        st_btn.click(force=True)
        page.wait_for_timeout(1000)

    # Scroll down thoroughly
    for _ in range(6):
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(400)

    full_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    print(f"Scrolled text length: {len(full_text)}")
    with open("scratch/full_page_with_b2.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    # Check Block 2
    if "Block 2 Responses:" in full_text:
        idx = full_text.find("Block 2 Responses:")
        b2 = full_text[idx:]
        print("\n=== BLOCK 2 OUTPUT ===")
        print(b2[:2500])
    elif "Block 2" in full_text:
        idx = full_text.find("Block 2")
        print("\n=== BLOCK 2 OUTPUT ===")
        print(full_text[idx:idx+2500])

    page.screenshot(path="scratch/live_b2_scrolled_view.png")
    print("Screenshot saved to scratch/live_b2_scrolled_view.png")
