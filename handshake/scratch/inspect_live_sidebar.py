import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # Let's inspect the entire feedback sidebar structure
    res = page.evaluate("""() => {
        const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            disabled: b.disabled,
            ariaLabel: b.getAttribute('aria-label'),
            className: b.className,
            rect: {
                x: b.getBoundingClientRect().x,
                y: b.getBoundingClientRect().y,
                width: b.getBoundingClientRect().width,
                height: b.getBoundingClientRect().height,
            }
        }));

        // Find elements with text 'Start'
        const startBtns = buttons.filter(b => b.text.toLowerCase() === 'start');

        // Find feedback items
        const feedbackContainer = document.querySelector('[class*="feedback" i], [data-testid*="feedback" i]');
        
        // Find all svg or icon buttons inside feedback panel
        const allSvgs = Array.from(document.querySelectorAll('svg')).map(s => {
            const p = s.closest('button') || s.parentElement;
            return {
                parentTag: p ? p.tagName : null,
                parentText: p ? p.innerText.trim() : null,
                parentClass: p ? p.className : null,
                rect: s.getBoundingClientRect()
            };
        });

        return {
            buttonsCount: buttons.length,
            startBtns,
            sidebarButtons: buttons.filter(b => b.rect.x > 700),
            allButtons: buttons.filter(b => b.text.length > 0)
        };
    }""")

    print(f"Total buttons: {res['buttonsCount']}")
    print("\nStart buttons:")
    for b in res["startBtns"]:
        print(" ", b)
    print("\nSidebar buttons (x > 700):")
    for b in res["sidebarButtons"]:
        print(" ", b)
    print("\nAll labeled buttons:")
    for b in res["allButtons"]:
        print(" ", b)
