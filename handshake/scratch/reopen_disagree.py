import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    # Click the circle-slash icon button
    btn = pg.locator("button[aria-label='Disagree']:visible").first
    print("Disagree button count:", btn.count())
    if btn.count() > 0:
        btn.click()
    else:
        # Click by coords
        pg.mouse.click(1174, 252) # check y of circle slash
    time.sleep(1)
    
    # Inspect inputs inside the sidebar
    info = pg.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('input, textarea'));
        return els.map(e => ({
            tag: e.tagName,
            type: e.type,
            placeholder: e.placeholder,
            value: e.value,
            rect: e.getBoundingClientRect()
        }));
    }""")
    print("Inputs after click:", info)
    pg.screenshot(path="scratch/after_card_reopen.png")
