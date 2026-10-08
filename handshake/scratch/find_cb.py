import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    html = pg.evaluate("""() => {
        const p = Array.from(document.querySelectorAll('p')).find(e => e.innerText.includes('These statements must all be true'));
        if (!p) return 'Not found';
        let curr = p;
        for (let i = 0; i < 6; i++) {
            if (curr.parentElement) curr = curr.parentElement;
        }
        return curr.outerHTML;
    }""")
    print("Outer container HTML length:", len(html))
    with open("scratch/checkbox_container.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Saved scratch/checkbox_container.html")
