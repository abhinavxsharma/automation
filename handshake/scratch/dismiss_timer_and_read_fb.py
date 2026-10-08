import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    b = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = b.contexts[0].pages[0]
    
    # 1. Click Start timer
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        box = st.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            print("Clicked Start timer")
            page.wait_for_timeout(2000)
    
    page.screenshot(path="scratch/after_dismiss_timer_1520.png")
    
    # 2. Extract all feedback items from the sidebar
    fb_text = page.evaluate("""() => {
        const sidebar = document.querySelector('[class*=\"sidebar\"], [class*=\"Sidebar\"]');
        return sidebar ? sidebar.innerText : document.body.innerText;
    }""")
    
    Path("scratch/fb_sidebar_live.txt").write_text(fb_text, encoding="utf-8")
    print("Feedback text length:", len(fb_text))
    print("Feedback text preview:\n", fb_text[:800])
