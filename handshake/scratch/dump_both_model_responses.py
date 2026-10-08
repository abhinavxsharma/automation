import sys
import time

from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    for _ in range(20):
        text = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Block 1" in text or "Final Answer" in text:
            break
        time.sleep(0.5)

    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(500)

    full_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/both_model_responses.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    # Let's extract Block 1 and Block 2 text cleanly
    b1_start = full_text.find("Block 1 Responses:")
    b2_start = full_text.find("Block 2 Responses:")
    fa_start = full_text.find("Final Answer:")

    if b1_start != -1 and b2_start != -1:
        b1_text = full_text[b1_start:b2_start]
        b2_text = full_text[b2_start:fa_start] if fa_start != -1 else full_text[b2_start:]

        print("=== BLOCK 1 RESPONSE ===")
        print(b1_text[:600])
        print("...\n[End of B1 preview]")

        # Find boxed or final answer in B1
        for ln in b1_text.splitlines():
            if "boxed" in ln or "maximum flow" in ln.lower() or "throughput" in ln.lower():
                print("  B1 key line:", ln.strip()[:100])

        print("\n=== BLOCK 2 RESPONSE ===")
        print(b2_text[:600])
        print("...\n[End of B2 preview]")

        # Find boxed or final answer in B2
        for ln in b2_text.splitlines():
            if "boxed" in ln or "maximum flow" in ln.lower() or "throughput" in ln.lower():
                print("  B2 key line:", ln.strip()[:100])
