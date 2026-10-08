import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    info = pg.evaluate("""() => {
        const cbs = Array.from(document.querySelectorAll('input[type="checkbox"], button[role="checkbox"], [aria-checked]'));
        return cbs.map(cb => ({
            tag: cb.tagName,
            type: cb.type,
            checked: cb.checked,
            ariaChecked: cb.getAttribute('aria-checked'),
            name: cb.name,
            id: cb.id,
            parentText: cb.parentElement ? cb.parentElement.innerText.slice(0, 100) : ''
        }));
    }""")
    for item in info:
        print(item)
