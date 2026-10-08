import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const h = Array.from(document.querySelectorAll('*')).find(el => el.innerText && el.innerText.trim() === 'Error Type');
        if (!h) return 'No header Error Type found';
        const card = h.closest('div[class*="rounded"], div.border, section') || h.parentElement.parentElement;
        
        // Find all clickable elements, inputs, radios, or list items
        const clickables = Array.from(card.querySelectorAll('input, button, [role="radio"], [role="option"], li, label')).map(el => ({
            tag: el.tagName,
            type: el.type,
            role: el.getAttribute('role'),
            text: el.innerText ? el.innerText.substring(0, 80).replace(/\\n+/g, ' ') : '',
            checked: el.checked,
            ariaChecked: el.getAttribute('aria-checked'),
            className: el.className
        }));
        
        return {
            cardHTML: card.innerHTML.substring(0, 800),
            clickables
        };
    }""")
    print("Clickables:")
    for c in info['clickables']:
        print(" ", c)
