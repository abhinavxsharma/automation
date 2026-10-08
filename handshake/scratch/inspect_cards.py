import json
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    data = page.evaluate("""() => {
        const editButtons = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        return editButtons.map((btn, index) => {
            // Find preceding heading or relevant text
            let walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
            // Let's get the card element: go up until element has border or margin or is a direct section
            let node = btn;
            let card = null;
            while (node && node !== document.body) {
                if (node.tagName === 'SECTION' || node.classList.contains('border') || node.classList.contains('rounded-lg') || node.classList.contains('p-4') || node.classList.contains('p-6')) {
                    card = node;
                    break;
                }
                node = node.parentElement;
            }
            if (!card) card = btn.parentElement.parentElement;
            
            // Text inside this card excluding other cards
            let text = card ? card.innerText : '';
            return {
                index,
                textSnippet: text.substring(0, 250).replace(/\\n+/g, ' ')
            };
        });
    }""")

    for r in data:
        print(f"Btn {r['index']}: {r['textSnippet']}")
