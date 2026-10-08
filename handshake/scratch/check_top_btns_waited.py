import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button", timeout=10000)
    page.wait_for_timeout(1000)
    
    # 1. Dismiss timer modal if present
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)
    
    # Check all buttons in the document
    btns = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('header button, nav button, div.sticky button, [class*=\"header\"] button, button')).map((b, i) => ({
            i,
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            title: b.getAttribute('title') || '',
            rect: b.getBoundingClientRect()
        })).filter(b => b.rect.top >= 0 && b.rect.bottom <= 70);
    }""")
    print("Found top bar buttons:", len(btns))
    for b_item in btns:
        print(b_item)
