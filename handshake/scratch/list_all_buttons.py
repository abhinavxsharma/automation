import sys

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_selector("text=Computer Systems", timeout=10000)
    btns = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button, svg, [role="button"]')).map(b => ({
            tag: b.tagName,
            text: b.innerText ? b.innerText.trim() : '',
            aria: b.getAttribute('aria-label'),
            title: b.getAttribute('title'),
            cls: b.className ? (typeof b.className === 'string' ? b.className : b.className.baseVal) : ''
        })).filter(b => b.text || b.aria || b.title);
    }""")
    print("Total button-like elements:", len(btns))
    for i, b in enumerate(btns[:40]):
        print(
            f"El {i} ({b['tag']}): text={b['text']!r}, aria={b['aria']!r}, title={b['title']!r}"
        )
