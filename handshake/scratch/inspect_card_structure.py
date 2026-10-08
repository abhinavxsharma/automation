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
        
        const inputs = Array.from(card.querySelectorAll('input, select, textarea')).map(inp => ({
            name: inp.name,
            type: inp.type,
            value: inp.value,
            checked: inp.checked,
            required: inp.required
        }));
        
        // Also check any React Fiber key
        const fiberKey = Object.keys(card).find(k => k.startsWith('__reactFiber') || k.startsWith('__reactInternalInstance'));
        
        return {
            cardTag: card.tagName,
            inputs,
            fiberKey: !!fiberKey
        };
    }""")
    print("Card structure:", info)
