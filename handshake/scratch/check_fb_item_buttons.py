import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("[data-feedback-item-id]", timeout=10000)
    
    details = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('[data-feedback-item-id]'));
        return els.map(el => {
            const btns = Array.from(el.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                title: b.getAttribute('title'),
                cls: b.className
            }));
            return {
                id: el.getAttribute('data-feedback-item-id'),
                text: el.innerText.slice(0, 100).replace(/\\n/g, ' '),
                btns
            };
        });
    }""")
    for d in details:
        print(f"\nID: {d['id']}")
        print(f"Text: {d['text']}")
        print(f"Buttons: {d['btns']}")
