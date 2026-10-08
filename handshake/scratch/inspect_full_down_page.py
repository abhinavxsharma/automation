import time

from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Wait for page content
    for _ in range(20):
        text = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Algorithms" in text or "Enter your prompt" in text or "directed communication" in text:
            break
        time.sleep(0.5)

    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(1000)

    # Dump the full inner text of the page
    full_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_update_full.txt", "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"Full page text length: {len(full_text)} characters")

    # Let's find any text about responses or prompt
    lines = [ln.strip() for ln in full_text.splitlines() if ln.strip()]
    for i, ln in enumerate(lines):
        if any(kw in ln.lower() for kw in ["block", "response", "generation", "prompt", "statement", "checker"]):
            print(f"  Line {i}: {ln[:120]}")

    # Scroll down to prompt area and screenshot
    prompt_el = page.locator("text='directed communication network'").first
    if prompt_el.is_visible():
        prompt_el.scroll_into_view_if_needed()
        page.wait_for_timeout(1000)
        page.screenshot(path="scratch/scrolled_to_new_prompt.png")
        print("Saved scratch/scrolled_to_new_prompt.png")
    else:
        print("Prompt text element not directly visible by locator.")
        page.screenshot(path="scratch/scrolled_fallback.png")
