import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    tag = pg.evaluate("""() => {
        const el = document.querySelector('[placeholder="Add a resolve reason"]');
        return el ? { tag: el.tagName, type: el.type, className: el.className } : 'Not found';
    }""")
    print("Element tag:", tag)
