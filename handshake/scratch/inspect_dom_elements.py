from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Let's inspect the HTML of the main container
    elements = page.evaluate("""() => {
        const results = [];
        // Find all interactive or clickable elements with pencil, edit, or svg
        const allSvgs = document.querySelectorAll('svg');
        for (const svg of allSvgs) {
            const parent = svg.closest('button, div[role="button"], a') || svg.parentElement;
            const rect = svg.getBoundingClientRect();
            results.push({
                tag: svg.tagName,
                parentTag: parent ? parent.tagName : null,
                parentClass: parent ? parent.className : '',
                ariaLabel: svg.getAttribute('aria-label') || (parent ? parent.getAttribute('aria-label') : ''),
                rect: {x: rect.x, y: rect.y, width: rect.width, height: rect.height},
                visible: rect.width > 0 && rect.height > 0
            });
        }
        return results;
    }""")
    print(f"Total SVGs found: {len(elements)}")
    for i, el in enumerate(elements):
        if el['visible']:
            print(f"  SVG {i}: parent={el['parentTag']} class='{el['parentClass']}' aria='{el['ariaLabel']}' pos=({el['rect']['x']}, {el['rect']['y']})")
