import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    btns = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button')).map((b, idx) => ({
            idx,
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            title: b.getAttribute('title') || '',
            rect: b.getBoundingClientRect()
        })).filter(b => b.rect.y < 100);
    }""")
    print("Buttons in top 100px of page:")
    for b in btns:
        print(b)
