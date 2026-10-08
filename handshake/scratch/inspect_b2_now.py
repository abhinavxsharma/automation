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

    # Scroll down thoroughly
    for _ in range(6):
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(300)

    full_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    print(f"Total text length: {len(full_text)}")
    with open("scratch/page_with_b2_clean.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    if "Block 2 Responses:" in full_text:
        idx = full_text.find("Block 2 Responses:")
        b2 = full_text[idx:]
        print("=== BLOCK 2 OUTPUT ===")
        print(b2[:3000])

    page.screenshot(path="scratch/block2_clean_view.png")
    print("Saved scratch/block2_clean_view.png")
