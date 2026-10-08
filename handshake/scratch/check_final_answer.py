from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), None)
    if not page:
        page = next((pg for pg in browser.contexts[0].pages if "/task/" in pg.url), browser.contexts[0].pages[0])

    print("Connected to task page:", page.url)

    # Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=2000):
        st_btn.click()
        page.wait_for_timeout(1000)

    # Let's inspect the Final Answer input
    inp = page.locator("input[placeholder='Start typing...']").first
    if inp.is_visible():
        print("Final Answer input is visible!")
        # Let's check what value is in it
        print("Current input value:", inp.input_value())
    else:
        print("Final Answer input is NOT visible.")

    # Screenshot the current state
    page.screenshot(path="scratch/final_answer_state.png")
    print("Screenshot saved to scratch/final_answer_state.png")
