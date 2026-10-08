import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Check button aria-label="Feedback"
    fb_btn = page.locator("button[aria-label='Feedback']")
    print("Feedback header button count:", fb_btn.count())
    if fb_btn.count() > 0:
        print("Clicking Feedback header button...")
        fb_btn.first.click()
        page.wait_for_timeout(1000)

    # Check the sidebar class now
    sidebar_class = page.evaluate("""() => {
        const h3 = Array.from(document.querySelectorAll('h3')).find(e => e.innerText.trim() === 'Feedback');
        let curr = h3;
        while (curr && !curr.className.includes('bg-rosetta-bg-surface')) curr = curr.parentElement;
        return curr ? curr.className : 'Not found';
    }""")
    print("Sidebar class after click:", sidebar_class)
    page.screenshot(path="scratch/after_fb_btn_click.png")
