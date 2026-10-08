import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # Inspect the pencil edit buttons in the main review flow
    edit_buttons = page.evaluate("""() => {
        const edits = Array.from(document.querySelectorAll('button[aria-label="Edit this step"], [aria-label*="edit" i]')).map(b => {
            const card = b.closest('section, div[class*="card"], div[class*="container"]') || b.parentElement;
            return {
                aria: b.getAttribute('aria-label'),
                rect: b.getBoundingClientRect(),
                parentTextSnippet: (b.parentElement ? b.parentElement.parentElement.innerText : '').substring(0, 100).replace(/\\n/g, ' ')
            };
        });
        return edits;
    }""")

    print(f"Found {len(edit_buttons)} edit buttons on page:")
    for i, eb in enumerate(edit_buttons):
        print(f"  {i}: rect={eb['rect']['y']:.0f} | snippet: {eb['parentTextSnippet']}")
