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

    res = page.evaluate("""() => {
        // Find deepest card with 'Please resolve all QC error flags'
        const els = Array.from(document.querySelectorAll('*')).filter(el => 
            el.innerText && el.innerText.includes('Please resolve all QC error flags')
        );
        const card = els[els.length - 1];

        // Find inputs, textareas, buttons inside or near this card
        const cardParent = card ? card.closest('div[class*="rounded"], div[class*="card"], div[class*="shadow"]') || card.parentElement.parentElement : null;
        
        return {
            cardText: card ? card.innerText : null,
            cardHTML: cardParent ? cardParent.outerHTML.slice(0, 2000) : null,
            buttons: Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                visible: b.offsetParent !== null,
                enabled: !b.disabled,
                rect: b.getBoundingClientRect()
            })).filter(b => b.visible)
        };
    }""")

    print("Card text:")
    print(res['cardText'])
    print("\n--- Card HTML ---")
    print(res['cardHTML'])
    print("\n--- Visible Buttons ---")
    for b in res['buttons']:
        print(" ", b)
