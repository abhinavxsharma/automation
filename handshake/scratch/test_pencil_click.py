from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Let's find all pencil icons by looking for the buttons with pencil SVG
    # In earlier screenshot, below 'Algorithms and Complexity' at right side is a pencil icon.
    pencils = page.locator("button:has(svg)").all()
    print(f"Buttons with SVG: {len(pencils)}")
    for i, btn in enumerate(pencils):
        box = btn.bounding_box()
        text = btn.inner_text()
        print(f"  Btn {i}: box={box} text='{text}'")

    # Let's also look for SVG elements directly
    svgs = page.evaluate("""() => {
        const icons = [];
        for (const el of document.querySelectorAll('svg')) {
            const rect = el.getBoundingClientRect();
            icons.push({
                className: el.getAttribute('class'),
                parent: el.parentElement.tagName,
                parentClass: el.parentElement.className,
                rect: {x: rect.x, y: rect.y, w: rect.width, h: rect.height}
            });
        }
        return icons;
    }""")
    print(f"SVGs in DOM: {len(svgs)}")
    for s in svgs:
        if s['rect']['w'] > 0:
            print(" ", s)
