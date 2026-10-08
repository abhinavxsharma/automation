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

    # Dismiss timer modal
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click(force=True)
        page.wait_for_timeout(1000)

    # Scroll down thoroughly
    for _ in range(5):
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)

    text = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/live_page_scrolled_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Scrolled page text length: {len(text)}")
    if "Block 1 Responses:" in text:
        idx1 = text.find("Block 1 Responses:")
        idx2 = text.find("Block 2 Responses:") if "Block 2 Responses:" in text else len(text)
        print("=== BLOCK 1 SUMMARY ===")
        b1 = text[idx1:idx2]
        # Find boxed or final answer
        for line in b1.splitlines():
            if "boxed" in line or "critical path" in line.lower() or "answer" in line.lower():
                print("  ", line.strip())

    if "Block 2 Responses:" in text:
        idx2 = text.find("Block 2 Responses:")
        print("\n=== BLOCK 2 SUMMARY ===")
        b2 = text[idx2:]
        if "Generating response" in b2[:300]:
            print("Block 2 is STILL GENERATING...")
        else:
            print("Block 2 FINISHED GENERATING!")
            for line in b2.splitlines()[:50]:
                print("  ", line.strip())

    page.screenshot(path="scratch/after_scroll_b2.png")
