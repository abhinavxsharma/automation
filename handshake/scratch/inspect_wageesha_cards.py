import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)

    elements = page.evaluate("""() => {
        // Find elements with text Wageesha
        const wageeshas = Array.from(document.querySelectorAll('*')).filter(el => {
            return el.children.length === 0 && el.innerText && el.innerText.trim() === 'Wageesha';
        });

        return wageeshas.map((w, idx) => {
            let card = w.parentElement;
            for (let i = 0; i < 4; i++) {
                if (card && card.parentElement && card.parentElement.innerText.includes('Feedback')) {
                    break;
                }
                if (card && card.parentElement) card = card.parentElement;
            }

            const clickables = Array.from(card.querySelectorAll('button, [role="button"], svg')).map(c => {
                const rect = c.getBoundingClientRect();
                return {
                    tag: c.tagName,
                    role: c.getAttribute('role'),
                    aria: c.getAttribute('aria-label'),
                    rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) },
                    html: c.outerHTML.slice(0, 80)
                };
            });

            return {
                idx,
                cardText: card.innerText.replace(/\\n+/g, ' '),
                clickables
            };
        });
    }""")

    print("Wageesha cards info:")
    for c in elements:
        print(f"\n--- Card {c['idx']} ---")
        print(f"Text: {c['cardText'][:100]}")
        print("Clickables:")
        for cl in c["clickables"]:
            print(f"  {cl['tag']} aria='{cl['aria']}' role='{cl['role']}' rect={cl['rect']}")

    with open("scratch/feedback_card_clickables.json", "w", encoding="utf-8") as f:
        json.dump(elements, f, indent=2)
