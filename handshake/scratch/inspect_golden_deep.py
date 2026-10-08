import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)

    card_info = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('*')).filter(el => 
            el.innerText && el.innerText.includes('Golden Solution')
        );
        // Find deepest element
        let deepest = els[els.length - 1];
        
        // Find enclosing card
        let cur = deepest;
        let card = null;
        while (cur && cur !== document.body) {
            if (cur.querySelector('button')) {
                card = cur;
                break;
            }
            cur = cur.parentElement;
        }

        return {
            matchesCount: els.length,
            deepestTag: deepest ? deepest.tagName : null,
            deepestText: deepest ? deepest.innerText.slice(0, 100) : null,
            cardHTML: card ? card.outerHTML.slice(0, 3000) : null
        };
    }""")

    print("Matches count:", card_info['matchesCount'])
    print("Deepest tag:", card_info['deepestTag'])
    print("Deepest text:", card_info['deepestText'])
    print("\n--- Card HTML snippet ---")
    print(card_info['cardHTML'])
