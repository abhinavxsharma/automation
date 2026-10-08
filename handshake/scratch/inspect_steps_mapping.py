import json
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Let's evaluate in JS to find all sections, cards, labels, and edit buttons
    data = page.evaluate("""() => {
        const results = [];
        const editButtons = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        
        editButtons.forEach((btn, index) => {
            // Find closest section / card / container
            let container = btn.closest('[data-testid], [class*="card"], [class*="step"], section, form') || btn.parentElement;
            // Let's traverse up a few levels to find the meaningful heading or container
            let p = btn;
            let title = '';
            for (let i = 0; i < 5 && p; i++) {
                p = p.parentElement;
                if (!p) break;
                const h = p.querySelector('h1, h2, h3, h4, h5, h6, [class*="title"], [class*="label"], [class*="header"]');
                if (h && h.innerText.trim()) {
                    title = h.innerText.trim();
                    break;
                }
            }
            
            // Get text snippet around the button
            const directText = (btn.parentElement ? btn.parentElement.innerText : '').substring(0, 150);
            const containerText = (container ? container.innerText : '').substring(0, 300);
            
            results.push({
                index,
                title,
                directText,
                containerText: containerText.replace(/\\n+/g, ' ')
            });
        });
        return results;
    }""")

    for r in data:
        print(f"\n[Button {r['index']}] Title: '{r['title']}'")
        print(f"  Container: {r['containerText'][:150]}...")
