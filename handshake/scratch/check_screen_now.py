from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=2000):
        st_btn.click()
        page.wait_for_timeout(1000)

    # Let's inspect the entire scroll height and position
    scroll_info = page.evaluate("""() => {
        const el = document.scrollingElement || document.documentElement;
        return {
            scrollTop: el.scrollTop,
            scrollHeight: el.scrollHeight,
            clientHeight: el.clientHeight
        };
    }""")
    print("Scroll info:", scroll_info)

    # Scroll to bottom to see current step clearly
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1000)
    page.screenshot(path="scratch/step_bottom.png")
    print("Bottom screenshot saved: scratch/step_bottom.png")

    # Find the current active step / input card
    card_text = page.locator("div:has-text('Final Answer')").last.inner_text()
    print("Card text preview:\n", card_text[:300])
