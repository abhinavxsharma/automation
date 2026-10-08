import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button", timeout=10000)
    all_btns = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button')).map((b, i) => ({
            i,
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            cls: b.className
        }));
    }""")
    print("Total buttons on page:", len(all_btns))
    for b in all_btns:
        if b["text"] or b["aria"]:
            print(b)
