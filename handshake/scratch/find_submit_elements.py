import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    elements = page.locator("*:has-text('Submit')").all()
    print(f"Total elements containing 'Submit': {len(elements)}")
    for i, el in enumerate(elements):
        try:
            tag = el.evaluate("e => e.tagName")
            txt = el.inner_text().strip()
            vis = el.is_visible()
            if len(txt) < 50:
                print(f"  [{i}] tag={tag} vis={vis} text='{txt}' class='{el.get_attribute('class')}'")
        except Exception:
            pass
