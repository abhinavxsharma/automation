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

    print("Page hydrated. Monitoring Block 2 until completion...")

    for poll in range(60):  # poll up to 5 minutes
        # Scroll to bottom with null-safety
        page.evaluate("() => { if (document.body) window.scrollTo(0, document.body.scrollHeight); }")
        time.sleep(2)


        text = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Block 2 Responses:" in text:
            idx = text.find("Block 2 Responses:")
            b2_text = text[idx:]
            # Check if finished
            first_lines = b2_text[:400]
            if "Generating response" not in first_lines:
                print(f"\n>>> BLOCK 2 FINISHED at poll {poll}!")
                print("=== BLOCK 2 RESPONSE ===")
                print(b2_text[:2500])
                with open("scratch/block2_completed_output.txt", "w", encoding="utf-8") as f:
                    f.write(b2_text)
                break
            else:
                if poll % 3 == 0:
                    print(f"  [Poll {poll}] Block 2 still generating...")

        time.sleep(3)

    page.screenshot(path="scratch/after_b2_finished.png")
    print("Screenshot saved to scratch/after_b2_finished.png")
