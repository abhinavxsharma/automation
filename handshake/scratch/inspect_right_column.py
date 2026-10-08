import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    right_elements = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('*'));
        return els
            .filter(e => {
                const r = e.getBoundingClientRect();
                return r.left > 750 && r.width > 50 && r.height > 20 && e.innerText && e.innerText.trim();
            })
            .map(e => ({
                tag: e.tagName,
                className: e.className,
                rect: e.getBoundingClientRect(),
                text: e.innerText.trim().slice(0, 150)
            }));
    }""")
    print("Right elements count:", len(right_elements))
    for i, el in enumerate(right_elements[:15]):
        print(f"[{i}] {el['tag']} ({el['rect']['left']}, {el['rect']['top']}) : {repr(el['text'][:60])}")
