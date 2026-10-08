import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    pg.wait_for_timeout(2000)
    btns = pg.locator("button, a").all()
    for i in [2, 6]:
        print(f"[{i}]:", btns[i].evaluate("e => e.outerHTML"))
