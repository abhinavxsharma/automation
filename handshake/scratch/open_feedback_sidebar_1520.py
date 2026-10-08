import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    
    # Click the feedback toggle button (the checklist icon in top nav)
    # Let's find button with aria-label or containing svg
    fb_toggle = page.locator("button[aria-label*='Feedback'], button[aria-label*='feedback'], button:has(svg path[d*='M2'])").first
    # Or find all top nav buttons
    top_nav_btns = page.locator("div.flex.h-\\[56px\\] button").all()
    print("Top nav buttons count:", len(top_nav_btns))
    for i, btn in enumerate(top_nav_btns):
        print(f"[{i}] aria={btn.get_attribute('aria-label')}, text={btn.inner_text().strip()}")
    
    # Usually button with aria-label="Feedback" or the 4th/5th button
    fb_btn = page.locator("button[aria-label='Feedback'], button[aria-label='Reviewer feedback']").first
    if not fb_btn.is_visible():
        # Let's click the button next to Tx
        for btn in top_nav_btns:
            aria = btn.get_attribute("aria-label") or ""
            if "feedback" in aria.lower() or "checklist" in aria.lower():
                fb_btn = btn
                break
    
    if fb_btn.is_visible():
        print("Clicking feedback button...")
        fb_btn.click()
    else:
        # Fallback: click the icon button between Tx and ?
        print("Clicking top nav button index 4...")
        if len(top_nav_btns) >= 5:
            top_nav_btns[4].click()
            
    page.wait_for_timeout(2000)
    page.screenshot(path="scratch/feedback_opened_1520.png")
    
    # Read sidebar text
    txt = page.evaluate("""() => {
        const sidebar = document.querySelector('[class*=\"sidebar\"], [class*=\"Sidebar\"]');
        return sidebar ? sidebar.innerText : 'NO_SIDEBAR';
    }""")
    Path("scratch/fb_sidebar_text.txt").write_text(txt, encoding="utf-8")
    print("Sidebar text length:", len(txt))
    print("Sidebar preview:\n", txt[:600])
