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
    page.wait_for_timeout(1000)
    
    # Check all feedback items
    items = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('[data-feedback-item-id]'));
        return els.map(el => ({
            id: el.getAttribute('data-feedback-item-id'),
            text: el.innerText.slice(0, 100).replace(/\\n/g, ' ')
        }));
    }""")
    print("Feedback items in DOM:", len(items))
    for it in items:
        print(it)
