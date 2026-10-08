from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=3000):
        st_btn.click()
        page.wait_for_timeout(1000)

    html = page.content()
    with open("scratch/page.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Dumped page HTML ({len(html)} bytes) to scratch/page.html")
