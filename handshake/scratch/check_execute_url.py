import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    
    # Check current URL
    print("Initial URL:", page.url)
    
    # Navigate to the execute URL provided in the notification
    exec_url = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/execute"
    print("Navigating to:", exec_url)
    page.goto(exec_url)
    page.wait_for_timeout(3000)

    # Dismiss timer if present
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        b = st.bounding_box()
        if b:
            page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
            page.wait_for_timeout(1000)

    print("Current URL after navigation:", page.url)
    print("Current Title:", page.title())
    page.screenshot(path="handshake/scratch/execute_page_view.png")
    print("Screenshot saved to handshake/scratch/execute_page_view.png")

    body_text = page.locator("body").inner_text()
    with open("handshake/scratch/execute_body_text.txt", "w", encoding="utf-8") as f:
        f.write(body_text)
    print("Body text snippet:\n", body_text[:600])
