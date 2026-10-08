import sys

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const ta = document.querySelector('textarea');
        const container = ta.parentElement.parentElement;
        const imgs = Array.from(container.querySelectorAll('img')).map(img => ({
            src: img.src.substring(0, 100),
            rect: img.getBoundingClientRect()
        }));
        
        const allBtns = Array.from(container.querySelectorAll('button')).map(b => ({
            text: b.innerText,
            aria: b.getAttribute('aria-label'),
            title: b.getAttribute('title'),
            cls: b.className,
            rect: b.getBoundingClientRect()
        }));
        
        return { imgs, allBtns };
    }""")
    print("Images:", info["imgs"])
    print("Buttons inside editor container:")
    for b in info["allBtns"]:
        print(
            f"  Text={b['text']!r}, aria={b['aria']!r}, rect=({b['rect']['x']}, {b['rect']['y']})"
        )
