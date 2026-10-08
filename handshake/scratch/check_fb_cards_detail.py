import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)
    
    # Inspect feedback cards
    cards = page.evaluate("""() => {
        // Find right panel container
        const items = [];
        // Look for cards inside the feedback container
        // In the screenshot, each item has an icon, title, author, text, and action buttons
        const actionBtns = Array.from(document.querySelectorAll('button[aria-label=\"Resolve\"], button[aria-label=\"Disagree\"], button[title=\"Resolve\"], button[title=\"Disagree\"]'));
        
        // Find all cards containing feedback
        const allCardEls = Array.from(document.querySelectorAll('div')).filter(d => 
            d.innerText && (d.innerText.includes('Jimson') || d.innerText.includes('Science Judge')) && d.children.length >= 2
        );
        
        return allCardEls.map(c => ({
            text: c.innerText.slice(0, 200).replace(/\\n/g, ' -- '),
            buttons: Array.from(c.querySelectorAll('button')).map(b => ({
                aria: b.getAttribute('aria-label'),
                text: b.innerText,
                cls: b.className
            }))
        }));
    }""")
    print("Found feedback card candidates:", len(cards))
    for i, c in enumerate(cards):
        print(f"[{i}] {c}")
