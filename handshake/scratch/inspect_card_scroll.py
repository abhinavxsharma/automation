import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Continue');
        if (!btn) return 'No continue button found';
        
        let p = btn;
        let card = null;
        for (let i = 0; i < 10 && p; i++) {
            p = p.parentElement;
            if (p && p.innerText && p.innerText.includes('Select the error type')) {
                card = p;
                break;
            }
        }
        if (!card) return 'Card not found';

        return {
            fullText: card.innerText,
            allTags: Array.from(card.querySelectorAll('*')).map(el => ({
                tag: el.tagName,
                type: el.type,
                name: el.name,
                text: el.innerText ? el.innerText.trim().slice(0, 40) : '',
                aria: el.getAttribute('aria-label')
            })).filter(e => e.type || e.aria || ['INPUT', 'TEXTAREA', 'SELECT', 'BUTTON'].includes(e.tag))
        };
    }""")
    print("Full text inside card:\n", info['fullText'])
    print("\nAll input/button tags:")
    for t in info['allTags']:
        print(" ", t)
