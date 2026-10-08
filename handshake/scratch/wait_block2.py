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

    # Dismiss timer modal
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=500):
        st_btn.click(force=True)
        page.wait_for_timeout(500)

    print("Waiting for Block 2 to finish generating...")
    for i in range(40):  # poll up to ~3.5 minutes
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        text = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Block 2 Responses:" in text:
            idx = text.find("Block 2 Responses:")
            b2_snippet = text[idx:]
            if "Generating response" not in b2_snippet[:300]:
                print(f"Block 2 finished generating at check {i}!")
                with open("scratch/block2_full_response.txt", "w", encoding="utf-8") as f:
                    f.write(b2_snippet)
                break
            else:
                if i % 2 == 0:
                    print(f"  [Check {i}] Block 2 still generating...")
        time.sleep(4)

    page.screenshot(path="scratch/after_b2_done.png")
    print("Screenshot saved to scratch/after_b2_done.png")
