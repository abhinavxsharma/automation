import sys
import time

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

def main():
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
        page = browser.contexts[0].pages[0]

        print("Monitoring Model Generations...")

        # Monitor Block 1
        for poll in range(60):  # up to 5 minutes
            text = page.evaluate("() => document.body ? document.body.innerText : ''")
            if "Block 1 Responses:" in text:
                # Check if still generating
                # In Block 1, "Generating response" indicates in-progress
                sub_text = text[text.find("Block 1 Responses:"):]
                first_500 = sub_text[:500]
                if "Generating response" not in first_500:
                    print(f"Block 1 finished generating (poll {poll})!")
                    break
                else:
                    if poll % 4 == 0:
                        print(f"  [Poll {poll}] Block 1 still generating...")
            time.sleep(5)

        page.wait_for_timeout(2000)
        # Check for Continue button to trigger Block 2
        cont_btn = page.locator("button:has-text('Continue')").first
        if cont_btn.is_visible(timeout=3000):
            print("Found Continue button after Block 1! Clicking it to trigger Block 2...")
            cont_btn.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            cont_btn.click(force=True)
            page.wait_for_timeout(3000)

        # Monitor Block 2
        for poll in range(60):
            text = page.evaluate("() => document.body ? document.body.innerText : ''")
            if "Block 2 Responses:" in text or "Block 2" in text:
                sub_text = text[text.find("Block 2"):]
                first_500 = sub_text[:500]
                if "Generating response" not in first_500:
                    print(f"Block 2 finished generating (poll {poll})!")
                    break
                else:
                    if poll % 4 == 0:
                        print(f"  [Poll {poll}] Block 2 still generating...")
            time.sleep(5)

        page.wait_for_timeout(2000)
        # Final full text dump
        full_text = page.evaluate("() => document.body ? document.body.innerText : ''")
        with open("scratch/both_model_responses_dag.txt", "w", encoding="utf-8") as f:
            f.write(full_text)

        page.screenshot(path="scratch/after_both_models_dag.png")
        print("Completed monitoring! Screenshot saved to scratch/after_both_models_dag.png")

if __name__ == "__main__":
    main()
