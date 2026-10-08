import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Check next button
    next_btn = page.locator("button:has-text('Next')").first
    print("Next button visible:", next_btn.is_visible())
    print("Next button disabled:", next_btn.is_disabled())

    # Check all elements below step 8
    elements = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        return {
            bodyLength: bodyText.length,
            snippets: bodyText.split('\\n').filter(l => l.trim()).slice(-30)
        };
    }""")
    print("End of page text:")
    for l in elements['snippets']:
        print(" ", l)
