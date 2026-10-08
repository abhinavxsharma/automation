from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    elements = page.evaluate("""() => {
        const results = [];
        const all = document.querySelectorAll('*');
        for (const el of all) {
            if (el.scrollHeight > el.clientHeight + 20 && el.clientHeight > 100) {
                results.push({
                    tag: el.tagName,
                    id: el.id,
                    className: (el.className || '').toString().slice(0, 50),
                    scrollHeight: el.scrollHeight,
                    clientHeight: el.clientHeight,
                    scrollTop: el.scrollTop
                });
            }
        }
        return results;
    }""")
    print(f"Elements with scrollHeight > clientHeight: {len(elements)}")
    for e in elements:
        print(" ", e)
