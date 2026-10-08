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

    # Click Start timer button
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=2000):
        print("Clicking 'Start timer' to resume timer and clear modal...")
        st_btn.click(force=True)
        page.wait_for_timeout(2000)

    # Poll for Block 1 completion
    print("Waiting for Block 1 to finish generating...")
    for i in range(30):  # poll up to ~2.5 minutes
        text = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Block 1 Responses:" in text:
            idx = text.find("Block 1 Responses:")
            snippet = text[idx:idx+400]
            if "Generating response" not in snippet:
                print(f"Block 1 finished generating at check {i}!")
                print("Snippet:", snippet[:300])
                break
            else:
                print(f"  Check {i}: Block 1 still generating...")
        time.sleep(5)

    # Dump full text
    full_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/block1_poll_text.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    page.screenshot(path="scratch/after_b1_poll.png")
    print("Screenshot saved to scratch/after_b1_poll.png")
