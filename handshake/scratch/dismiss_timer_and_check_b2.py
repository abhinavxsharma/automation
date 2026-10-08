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

    # Click Start timer to resume timer and clear modal
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=2000):
        print("Clicking 'Start timer'...")
        st_btn.click(force=True)
        page.wait_for_timeout(1500)

    # Dismiss any other toast
    got_it = page.locator("button:has-text('Got it')").first
    if got_it.is_visible(timeout=500):
        got_it.click(force=True)
        page.wait_for_timeout(500)

    # Scroll down to reveal Block 2
    for _ in range(4):
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)

    # Get body text
    body_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/block2_scrolled_text.txt", "w", encoding="utf-8") as f:
        f.write(body_text)

    if "Block 2 Responses:" in body_text:
        idx = body_text.find("Block 2 Responses:")
        b2 = body_text[idx:]
        print("=== BLOCK 2 OUTPUT ===")
        print(b2[:2000])
    elif "Block 2" in body_text:
        idx = body_text.find("Block 2")
        print("=== BLOCK 2 OUTPUT ===")
        print(body_text[idx:idx+2000])
    else:
        print("Block 2 text not found. Total body text length:", len(body_text))

    page.screenshot(path="scratch/block2_scrolled.png")
    print("Saved scratch/block2_scrolled.png")
