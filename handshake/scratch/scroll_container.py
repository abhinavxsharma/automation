from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Find the element with overflow-y: auto / scroll
    scroll_res = page.evaluate("""() => {
        const all = document.querySelectorAll('*');
        const scrollables = [];
        for (const el of all) {
            const style = window.getComputedStyle(el);
            if ((style.overflowY === 'auto' || style.overflowY === 'scroll') && el.scrollHeight > el.clientHeight) {
                scrollables.push({
                    tag: el.tagName,
                    className: el.className,
                    scrollHeight: el.scrollHeight,
                    clientHeight: el.clientHeight,
                    scrollTop: el.scrollTop
                });
                // Scroll it to bottom
                el.scrollTop = el.scrollHeight;
            }
        }
        return scrollables;
    }""")
    print("Scrollables:", scroll_res)
    page.wait_for_timeout(1000)
    page.screenshot(path="scratch/inner_scrolled_bottom.png")
    print("Saved scratch/inner_scrolled_bottom.png")
