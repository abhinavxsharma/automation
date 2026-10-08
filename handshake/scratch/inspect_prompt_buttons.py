import sys
import time

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Let's find all buttons or icons near the prompt
    res = page.evaluate("""() => {
        const text = 'Determine the fully simplified';
        const els = Array.from(document.querySelectorAll('*')).filter(el => el.innerText && el.innerText.includes(text));
        const deepEl = els[els.length - 1];
        const container = deepEl.parentElement.parentElement;
        const btns = Array.from(container.querySelectorAll('button, svg, [role="button"]')).map(b => ({
            tag: b.tagName,
            aria: b.getAttribute('aria-label'),
            text: b.innerText,
            rect: b.getBoundingClientRect()
        }));
        return {
            containerText: container.innerText.substring(0, 100),
            btns
        };
    }""")
    print("Container text:", res["containerText"])
    print("Buttons found near prompt:")
    for b in res["btns"]:
        print(
            f"  Tag={b['tag']}, aria={b['aria']!r}, rect=({b['rect']['x']}, {b['rect']['y']}, {b['rect']['width']}, {b['rect']['height']})"
        )
