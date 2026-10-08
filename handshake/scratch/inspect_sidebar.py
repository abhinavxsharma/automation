import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # Inspect feedback sidebar
    sidebar_data = pg.evaluate('''() => {
        const sidebar = document.querySelector('aside, [role="complementary"]') || document.querySelector('[class*="Feedback"], [class*="feedback"]')?.closest('div');
        const cards = Array.from(document.querySelectorAll('[class*="card"], [class*="Card"], [class*="Item"], [class*="item"]'))
            .filter(el => el.innerText.includes('Jimson') || el.innerText.includes('Science Judge') || el.innerText.includes('Image quality') || el.innerText.includes('Minor issue'));
            
        const text = sidebar ? sidebar.innerText : document.body.innerText;
        
        // Find resolve / disagree buttons
        const actionBtns = Array.from(document.querySelectorAll('button'))
            .filter(b => b.getAttribute('aria-label') === 'Resolve' || b.getAttribute('aria-label') === 'Disagree' || b.innerText.includes('Resolve') || b.innerText.includes('Disagree'))
            .map((b, idx) => ({
                idx,
                aria: b.getAttribute('aria-label'),
                text: b.innerText.trim(),
                visible: b.offsetParent !== null
            }));

        return {
            sidebarSnippet: text.slice(0, 2000),
            cardsCount: cards.length,
            actionBtns
        };
    }''')
    
    print("Sidebar snippet:")
    print(sidebar_data["sidebarSnippet"][:1000])
    print("\nAction buttons in sidebar:")
    for b in sidebar_data["actionBtns"]:
        print(f"  [{b['idx']}] aria='{b['aria']}' text='{b['text']}' visible={b['visible']}")
