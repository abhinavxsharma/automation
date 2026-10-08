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

    # Dismiss modals
    for sel in ["button:has-text('Start timer')", "button:has-text('Got it')", "button:has-text('OK')"]:
        btn = page.locator(sel).first
        if btn.is_visible(timeout=500):
            btn.click(force=True)
            page.wait_for_timeout(500)

    text = page.evaluate("() => document.body ? document.body.innerText : ''")
    
    # Check if Block 1 finished
    if "Block 1 Responses:" in text:
        idx = text.find("Block 1 Responses:")
        b1_text = text[idx:idx+3000]
        if "Generating response" in b1_text[:300]:
            print("STATUS: Block 1 is STILL GENERATING...")
        else:
            print("STATUS: Block 1 GENERATION FINISHED!")
            print("=== BLOCK 1 SNIPPET ===")
            print(b1_text[:1500])
            with open("scratch/block1_output.txt", "w", encoding="utf-8") as f:
                f.write(b1_text)

            # Check if Continue button is visible
            cont_btn = page.locator("button:has-text('Continue')").first
            if cont_btn.is_visible(timeout=1000):
                print("Continue button is visible! Clicking to trigger Block 2...")
                cont_btn.scroll_into_view_if_needed()
                page.wait_for_timeout(500)
                cont_btn.click(force=True)
                page.wait_for_timeout(2000)

    page.screenshot(path="scratch/check_b1_live.png")
    print("Screenshot saved to scratch/check_b1_live.png")
