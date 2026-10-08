import json
import sys

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const ta = document.querySelector('textarea');
        if (!ta) return { error: 'no textarea' };
        
        const container = ta.closest('div[class*="rosetta"]') || ta.parentElement.parentElement;
        const btns = Array.from(container.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            cls: b.className,
            disabled: b.disabled || b.getAttribute('aria-disabled') === 'true'
        }));
        
        return {
            taValue: ta.value,
            btns,
            files: Array.from(document.querySelectorAll('input[type="file"]')).map(f => f.outerHTML)
        };
    }""")
    print("Card info:\n", json.dumps(info, indent=2))
