import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next(pg for pg in browser.contexts[0].pages if "1520c7f4" in pg.url)
    
    # Read feedback panel text and items
    fb_panel = page.locator("div.FeedbackSidebar-module__sR0nha__sidebarContainer, [aria-label='Feedback'], div:has(h3:has-text('Feedback')), div:has-text('Feedback')")
    
    # Get all cards in feedback panel
    cards_data = page.evaluate("""() => {
        const items = [];
        // Look for feedback list or cards
        const allDivs = Array.from(document.querySelectorAll('*'));
        // Find reviewer items
        const jimsons = allDivs.filter(d => d.innerText && d.innerText.includes('Jimson'));
        return jimsons.map(j => ({
            tag: j.tagName,
            text: j.innerText
        }));
    }""")
    
    print(f"Jimson items found: {len(cards_data)}")
    for i, c in enumerate(cards_data[:5]):
        print(f"--- Item {i} ---")
        print(c['text'])
    
    # Also dump the full text of the feedback sidebar
    sidebar_text = page.evaluate("""() => {
        const sb = document.querySelector('[class*=\"sidebar\"], [class*=\"Feedback\"]');
        return sb ? sb.innerText : document.body.innerText;
    }""")
    Path("scratch/fb_sidebar_full.txt").write_text(sidebar_text, encoding="utf-8")
    print("\nSidebar text written to scratch/fb_sidebar_full.txt")
