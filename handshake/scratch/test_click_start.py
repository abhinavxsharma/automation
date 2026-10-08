import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0:
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(500)

    # Click the Start button at the bottom of the sidebar
    start_btn = page.locator("button:has-text('Start')").last
    print("Start button visible?", start_btn.is_visible())
    start_btn.click()
    page.wait_for_timeout(1000)

    page.screenshot(path="scratch/after_start_clicked.png")

    # Inspect feedback panel now
    fb_text = page.evaluate("""() => {
        const body = document.body.innerText;
        const start = body.indexOf('Feedback');
        return start !== -1 ? body.slice(start, start + 1000) : '';
    }""")
    print("Feedback panel text after clicking Start:\n", fb_text)
