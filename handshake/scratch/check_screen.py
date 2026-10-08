import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    pg.screenshot(path="scratch/screen_state_check.png")
    txt = pg.evaluate("() => document.body ? document.body.innerText : ''")
    print("URL:", pg.url)
    print("Preview:\n", txt[:500])
