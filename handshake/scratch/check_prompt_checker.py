from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Check Prompt Checker aside
    checker = page.locator("aside, div:has-text('Prompt Checker')").first
    if checker.is_visible():
        print("--- Prompt Checker Live Panel ---")
        print(checker.inner_text()[:1500])
    else:
        print("Prompt Checker panel not found.")

    # Screenshot the live page showing both prompt and feedback
    page.screenshot(path="scratch/live_prompt_and_feedback.png")
    print("Saved scratch/live_prompt_and_feedback.png")
