import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const allBtns = Array.from(document.querySelectorAll('button')).map((b, i) => {
            const rect = b.getBoundingClientRect();
            return {
                i,
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label') || '',
                title: b.getAttribute('title') || '',
                rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) },
                html: b.innerHTML.slice(0, 100),
                disabled: b.disabled
            };
        }).filter(b => b.rect.x > 700 || b.rect.w > 0);

        return allBtns;
    }""")

    with open("scratch/all_right_buttons.json", "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)

    print(f"Total buttons: {len(info)}")
    right_sidebar_btns = [b for b in info if b['rect']['x'] > 700]
    print(f"Buttons on right (x > 700): {len(right_sidebar_btns)}")
    for b in right_sidebar_btns:
        print(f"x={b['rect']['x']}, y={b['rect']['y']}, text='{b['text']}', aria='{b['aria']}', html={b['html'][:50]}")
