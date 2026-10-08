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

    print("Monitoring Block 2...")
    for poll in range(60):  # poll up to 5 minutes
        # Check and dismiss timer modal if it pops up
        btn = page.locator("button:has-text('Start timer')").first
        box = btn.bounding_box()
        if box:
            print("  Dismissing timer modal...")
            page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
            time.sleep(1)

        # Scroll down
        page.evaluate("() => { if (document.body) window.scrollTo(0, document.body.scrollHeight); }")
        time.sleep(2)

        text = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Block 2 Responses:" in text:
            idx = text.find("Block 2 Responses:")
            b2 = text[idx:]
            # Check if actual solution generated
            if "Generating response" not in b2[:300] and "This may take a while" not in b2[:300]:
                print(f"\n>>> BLOCK 2 FULLY GENERATED at poll {poll}!")
                print("=== BLOCK 2 OUTPUT ===")
                print(b2[:2000])
                with open("scratch/block2_real_output.txt", "w", encoding="utf-8") as f:
                    f.write(b2)
                break
            else:
                if poll % 3 == 0:
                    print(f"  [Poll {poll}] Block 2 still generating...")

        time.sleep(3)

    page.screenshot(path="scratch/after_real_b2.png")
    print("Screenshot saved to scratch/after_real_b2.png")
