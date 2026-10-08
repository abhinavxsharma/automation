import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    
    # 1. Dismiss timer modal
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        b = st.bounding_box()
        if b:
            page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
            page.wait_for_timeout(1500)
            print("Clicked Start timer")
    
    # Take screenshot without modal
    page.screenshot(path="scratch/after_dismiss_timer_1520.png")
    
    # 2. Inspect Feedback panel
    # Click "Needs attention" tab first, then "All" tab
    needs_att = page.locator("button:has-text('Needs attention')").first
    if needs_att.is_visible():
        needs_att.click()
        page.wait_for_timeout(1000)
        page.screenshot(path="scratch/fb_needs_attention.png")
        t_needs = page.evaluate("""() => {
            const sb = document.querySelector('[class*=\"sidebar\"], [class*=\"Feedback\"]');
            return sb ? sb.innerText : 'NO_SIDEBAR';
        }""")
        Path("scratch/fb_needs_attention_text.txt").write_text(t_needs, encoding="utf-8")
        print("Needs attention text length:", len(t_needs))
    
    # Now click "All" tab
    all_tab = page.locator("button:has-text('All')").first
    if all_tab.is_visible():
        all_tab.click()
        page.wait_for_timeout(1000)
        page.screenshot(path="scratch/fb_all_tab.png")
        t_all = page.evaluate("""() => {
            const sb = document.querySelector('[class*=\"sidebar\"], [class*=\"Feedback\"]');
            return sb ? sb.innerText : 'NO_SIDEBAR';
        }""")
        Path("scratch/fb_all_tab_text.txt").write_text(t_all, encoding="utf-8")
        print("All tab text length:", len(t_all))
