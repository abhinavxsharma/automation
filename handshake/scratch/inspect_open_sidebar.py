import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(500)

    # 1. Dismiss timer if visible
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing timer modal...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Inspect buttons in sidebar
    buttons = page.evaluate("""() => {
        const rightButtons = Array.from(document.querySelectorAll('button, [role=\"tab\"], label')).filter(el => {
            const r = el.getBoundingClientRect();
            return r.x > 740 && r.y > 50;
        });

        return rightButtons.map(el => {
            const r = el.getBoundingClientRect();
            return {
                tag: el.tagName,
                role: el.getAttribute('role'),
                text: el.innerText ? el.innerText.trim() : '',
                aria: el.getAttribute('aria-label'),
                disabled: el.disabled,
                ariaDisabled: el.getAttribute('aria-disabled'),
                classes: typeof el.className === 'string' ? el.className.slice(0, 50) : '',
                x: Math.round(r.x),
                y: Math.round(r.y),
                w: Math.round(r.width),
                h: Math.round(r.height)
            };
        });
    }""")

    print(f"Found {len(buttons)} right sidebar elements:")
    for b in buttons:
        print(b)
