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

    # 1. Dismiss timer modal
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        print("Dismissing timer modal...")
        modal_btn.first.click()
        page.wait_for_timeout(1000)

    # 2. Inspect Feedback panel elements
    info = page.evaluate("""() => {
        // Find elements in feedback container
        const cards = Array.from(document.querySelectorAll('*')).filter(el => 
            el.innerText && el.innerText.includes('Image Description Checker') && el.children.length === 0
        ).map(el => ({ tag: el.tagName, text: el.innerText }));

        // Find all buttons in the right sidebar or with text
        const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            disabled: b.disabled,
            visible: b.offsetParent !== null,
            rect: b.getBoundingClientRect()
        }));

        // Find all edit pencil icons or buttons across page
        const editPencils = Array.from(document.querySelectorAll('button, svg, [role="button"]')).filter(el => {
            const aria = el.getAttribute('aria-label') || '';
            const title = el.getAttribute('title') || '';
            const txt = el.innerText || '';
            return aria.toLowerCase().includes('edit') || title.toLowerCase().includes('edit') || txt.toLowerCase().includes('edit');
        }).map(el => ({
            tag: el.tagName,
            aria: el.getAttribute('aria-label'),
            text: el.innerText,
            rect: el.getBoundingClientRect()
        }));

        // Search text for 'genuine content'
        const findingCard = Array.from(document.querySelectorAll('*')).find(el => 
            el.innerText && el.innerText.includes('approximately 157 words') && el.children.length > 2
        );

        return {
            cards,
            buttons: buttons.filter(b => b.visible && (b.rect.right > 700 || b.text.includes('Start') || b.text.includes('Next'))),
            editPencils,
            findingCardTag: findingCard ? findingCard.tagName : null,
            findingCardRect: findingCard ? findingCard.getBoundingClientRect() : null
        };
    }""")

    print("Feedback buttons:", info['buttons'])
    print("Edit pencils count:", len(info['editPencils']))
    for ep in info['editPencils']:
        print("  Pencil:", ep)
    print("Finding card rect:", info['findingCardRect'])
