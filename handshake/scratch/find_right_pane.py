import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    res = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('*')).filter(el => {
            const rect = el.getBoundingClientRect();
            return rect.left >= 800 && rect.width > 0 && rect.height > 0 && el.children.length === 0 && el.innerText.trim().length > 0;
        });
        return els.map(e => ({
            tag: e.tagName,
            text: e.innerText.trim().slice(0, 100),
            rect: e.getBoundingClientRect()
        }));
    }""")
    print("Right pane text elements count:", len(res))
    for r in res:
        print(f"  [{r['tag']}] ({r['rect']['x']:.0f}, {r['rect']['y']:.0f}) {r['text']}")
