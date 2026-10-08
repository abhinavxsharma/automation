import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(500)

    # Find all edit buttons
    edit_buttons = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label="Edit this step"]'));
        return btns.map((btn, index) => {
            // Find nearby text/heading
            let p = btn.parentElement;
            let nearbyText = "";
            for (let i = 0; i < 5; i++) {
                if (p) {
                    nearbyText = p.innerText.trim().slice(0, 150);
                    if (nearbyText.length > 30) break;
                    p = p.parentElement;
                }
            }
            const rect = btn.getBoundingClientRect();
            return {
                index,
                rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
                nearbyText: nearbyText.replace(/\\n+/g, ' ')
            };
        });
    }""")

    print(f"Found {len(edit_buttons)} 'Edit this step' buttons:")
    for b in edit_buttons:
        print(f"[{b['index']}] at y={b['rect']['y']:.0f}: {b['nearbyText'][:100]}")
