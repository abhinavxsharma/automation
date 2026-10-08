import sys

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    card_html = page.evaluate("""() => {
        const ta = document.querySelector('textarea');
        if (!ta) return 'no textarea';
        let p = ta.parentElement;
        while (p && p.tagName !== 'BODY') {
            if (p.className && (p.className.includes('card') || p.className.includes('rosetta') || p.className.includes('rounded'))) {
                return p.innerHTML;
            }
            p = p.parentElement;
        }
        return ta.parentElement.innerHTML;
    }""")
    with open("handshake/scratch/card_html_inspect.html", "w", encoding="utf-8") as f:
        f.write(card_html)
    print("Wrote card_html_inspect.html, length:", len(card_html))
