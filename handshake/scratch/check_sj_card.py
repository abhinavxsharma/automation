import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button", timeout=10000)
    
    # 1. Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(500)
    
    # Inspect Science Judge card
    sj_info = page.evaluate("""() => {
        const headers = Array.from(document.querySelectorAll('h3, h4, div, span')).filter(el => el.innerText && el.innerText.includes('Science Judge - Lumiere'));
        if (headers.length === 0) return 'No header found';
        const card = headers[0].closest('div.border, div.rounded, div.p-4, div.p-3') || headers[0].parentElement.parentElement;
        const allBtns = Array.from(card.querySelectorAll('button')).map(b => ({
            tag: b.tagName,
            aria: b.getAttribute('aria-label'),
            text: b.innerText,
            title: b.getAttribute('title'),
            cls: b.className,
            svg: b.querySelector('svg')?.outerHTML.slice(0, 100)
        }));
        return { cardText: card.innerText.slice(0, 200), buttons: allBtns };
    }""")
    print("Science Judge card info:", sj_info)
