import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)

    card_info = page.evaluate("""() => {
        // Find elements with 'Golden Solution'
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        let target = null;
        while ((node = walker.nextNode())) {
            if (node.nodeValue.includes('Golden Solution:')) {
                target = node.parentElement;
                break;
            }
        }
        if (!target) return { found: false };

        // Walk up to find the card container
        let card = target;
        while (card && !card.querySelector('button')) {
            card = card.parentElement;
        }

        return {
            found: true,
            targetTag: target.tagName,
            cardTag: card ? card.tagName : null,
            cardClasses: card ? card.className : null,
            cardOuterHTML: card ? card.outerHTML.slice(0, 2000) : null
        };
    }""")

    print("Card info:")
    for k, v in card_info.items():
        if k != 'cardOuterHTML':
            print(f" {k}: {v}")
    if card_info.get('cardOuterHTML'):
        print("\n--- Card HTML ---")
        print(card_info['cardOuterHTML'])
