import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Let's inspect all radio inputs, list items, or buttons inside the card
    card = page.locator("div:has-text('Select the error type')").first
    print("Found card text snippet:", card.inner_text()[:200])

    radios = card.locator("input[type='radio'], [role='radio'], li, label").all()
    print(f"Found {len(radios)} candidate items inside card.")
    for i, r in enumerate(radios[:10]):
        tag = r.evaluate("e => e.tagName")
        txt = r.inner_text().strip()[:80].replace('\n', ' ')
        cls = r.get_attribute("class") or ""
        print(f"  [{i}] tag={tag} class='{cls[:50]}' text='{txt}'")
