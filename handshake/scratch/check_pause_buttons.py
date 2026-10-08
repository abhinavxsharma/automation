import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    print("Page URL:", pg.url)
    print("Page Title:", pg.title())
    all_elements = pg.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('button, a, [role="button"]'));
        return els.map(e => ({
            tag: e.tagName,
            text: e.innerText ? e.innerText.trim() : '',
            aria: e.getAttribute('aria-label') || '',
            href: e.getAttribute('href') || ''
        }));
    }""")
    print(f"Total interactive elements: {len(all_elements)}")
    for el in all_elements:
        if any(w in el['text'].lower() or w in el['aria'].lower() for w in ['save', 'exit', 'pause', 'timer', 'leave', 'dashboard']):
            print(f"  MATCH: {el}")
    pg.screenshot(path="scratch/current_pause_inspect.png")
    print("Screenshot saved to scratch/current_pause_inspect.png")
