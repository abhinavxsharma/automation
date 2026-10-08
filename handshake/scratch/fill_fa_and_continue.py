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
    for _ in range(10):
        t = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Final Answer" in t:
            break
        time.sleep(0.5)

    print("Page ready with Final Answer card.")

    # Fill 76 into input
    inp = page.locator("input[placeholder='Start typing...']").first
    print("Filling '76' into Final Answer input...")
    inp.fill("76", force=True)
    page.wait_for_timeout(500)

    # Trigger React change events
    page.evaluate("""() => {
        const inp = document.querySelector("input[placeholder='Start typing...']");
        if (inp) {
            inp.value = "76";
            inp.dispatchEvent(new Event('input', { bubbles: true }));
            inp.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""")
    page.wait_for_timeout(500)

    # Click Continue button
    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_fa_continue.png")
    print("Saved scratch/after_fa_continue.png")

    # Inspect current text to see what next step is
    new_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in new_text.splitlines() if ln.strip()]
    print("\n--- Next Active Step Context ---")
    for ln in lines[-30:]:
        print(" ", ln)
