import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(1000)

    # Dismiss timer if visible
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(500)

    # Let's inspect sidebar items
    feedback_data = page.evaluate("""() => {
        const sidebar = document.querySelector("aside") || document.querySelector("[aria-label='Feedback']") || document.body;
        // Find all items/cards in sidebar
        const allTab = Array.from(document.querySelectorAll('button, [role=\"tab\"]')).find(el => el.innerText.trim() === 'All');
        const needsAttentionTab = Array.from(document.querySelectorAll('button, [role=\"tab\"]')).find(el => el.innerText.includes('Needs attention'));
        
        const cards = Array.from(document.querySelectorAll('div')).filter(d => {
            const t = d.innerText || '';
            return (t.includes('Science Judge') || t.includes('Prompt Checker') || t.includes('Reviewer') || t.includes('Admin')) && d.children.length > 0 && d.children.length < 10;
        });
        
        return {
            sidebarText: sidebar ? sidebar.innerText : '',
            allTab: allTab ? allTab.innerText : null,
            needsAttentionTab: needsAttentionTab ? needsAttentionTab.innerText : null
        };
    }""")
    print("Sidebar Feedback Data:")
    print("Needs Attention Tab:", feedback_data["needsAttentionTab"])
    print("All Tab:", feedback_data["allTab"])
    print("Sidebar Text:\n", feedback_data["sidebarText"])
