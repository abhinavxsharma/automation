import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    btns = pg.locator("button:has-text('Submit'), button:has-text('Next')").all()
    print("Bottom buttons found:")
    for b in btns:
        print(f"Text='{b.inner_text()}', aria='{b.get_attribute('aria-label')}', class='{b.get_attribute('class')}', box={b.bounding_box()}")
