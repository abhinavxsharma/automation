import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser, page = get_task_page(p)

    for i in range(20):
        if page.locator("button").count() > 5:
            break
        page.wait_for_timeout(500)

    res = page.evaluate("""() => {
        // Find element with text 'Image Description Checker'
        const all = Array.from(document.querySelectorAll('*'));
        const matches = all.filter(el => el.innerText && el.innerText.includes('Image Description Checker'));
        const deepest = matches[matches.length - 1];
        
        let card = deepest;
        while (card && !card.className.includes('rounded') && card.parentElement !== document.body) {
            card = card.parentElement;
        }

        return {
            deepestText: deepest ? deepest.innerText : null,
            cardClass: card ? card.className : null,
            cardHTML: card ? card.outerHTML.slice(0, 1500) : null
        };
    }""")

    print("Deepest text:", res['deepestText'])
    print("Card class:", res['cardClass'])
    print("Card HTML:\n", res['cardHTML'])
