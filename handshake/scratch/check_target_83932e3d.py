import sys
sys.path.insert(0, "scratch")
from chrome_helper import ensure_chrome, PORT
from playwright.sync_api import sync_playwright

target_url = "https://ai.joinhandshake.com/annotations/fellow/task/83932e3d-ea40-47e2-bc50-48cbef08fb3d/run"

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    print("Navigating to target task:", target_url)
    page.goto(target_url, timeout=30000)
    page.wait_for_timeout(3000)

    # Check for Start timer modal
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        b = st.bounding_box()
        if b:
            print("Dismissing timer modal via center click...")
            page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
            page.wait_for_timeout(1000)

    print("Current URL:", page.url)
    print("Current Title:", page.title())
    page.screenshot(path="scratch/target_task_83932e3d_initial.png")
    print("Screenshot saved to scratch/target_task_83932e3d_initial.png")

    body_text = page.locator("body").inner_text()
    print("\nBody text sample:\n", body_text[:600])
