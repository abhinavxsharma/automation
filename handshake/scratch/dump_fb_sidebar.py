import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    
    # Extract all text inside the feedback sidebar
    sidebar_info = page.evaluate("""() => {
        // Find sidebar container
        const allElements = Array.from(document.querySelectorAll('*'));
        const fbHeader = allElements.find(e => e.innerText && e.innerText.trim() === 'Feedback');
        let container = null;
        if (fbHeader) {
            container = fbHeader.closest('[class*=\"sidebar\"], [class*=\"container\"], [class*=\"Sidebar\"]') || fbHeader.parentElement.parentElement;
        }
        
        // Find all cards or items with reviewer names
        const cards = [];
        const possibleCards = document.querySelectorAll('[class*=\"card\"], [class*=\"item\"], [class*=\"FeedbackItem\"], [data-testid*=\"feedback\"]');
        possibleCards.forEach(c => {
            if (c.innerText && (c.innerText.includes('Jimson') || c.innerText.includes('Science Judge') || c.innerText.includes('Wageesha'))) {
                cards.push(c.innerText);
            }
        });
        
        return {
            fullText: container ? container.innerText : document.body.innerText,
            cards: cards
        };
    }""")
    
    print("--- FEEDBACK SIDEBAR TEXT ---")
    print(sidebar_info['fullText'])
    print("-----------------------------")
    Path("scratch/feedback_sidebar_dump.txt").write_text(sidebar_info['fullText'], encoding="utf-8")
