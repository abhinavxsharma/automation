import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser, page = get_task_page(p)

    for i in range(20):
        if page.locator("button").count() > 5:
            break
        page.wait_for_timeout(500)

    # Dismiss timer modal
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        modal_btn.first.click()
        page.wait_for_timeout(500)

    # Find the circle-slash icon next to Image Description Checker
    btn_info = page.evaluate("""() => {
        // Look in sidebar
        const sidebar = document.querySelector('aside') || document.querySelector('[class*="Feedback"]') || document.body;
        const findingHeader = Array.from(sidebar.querySelectorAll('*')).find(el => el.innerText && el.innerText.includes('Image Description Checker'));
        if (!findingHeader) return { error: 'header not found' };

        // Find enclosing card
        let card = findingHeader;
        while (card && !card.className.includes('rounded') && card !== document.body) {
            card = card.parentElement;
        }

        const buttons = Array.from(card.querySelectorAll('button, [role="button"], svg')).map(el => ({
            tag: el.tagName,
            aria: el.getAttribute('aria-label'),
            title: el.getAttribute('title'),
            classes: el.className,
            rect: el.getBoundingClientRect()
        }));

        return { cardText: card.innerText, buttons };
    }""")

    print("Card text in feedback:\n", btn_info.get('cardText'))
    print("\nButtons inside finding card:")
    for b in btn_info.get('buttons', []):
        print(" ", b)
