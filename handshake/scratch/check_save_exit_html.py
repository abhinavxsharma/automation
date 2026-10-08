import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    pg.wait_for_timeout(2000)
    save_btn = pg.get_by_role("button", name="Save")
    exit_btn = pg.get_by_role("button", name="Exit")
    print("Save btn:", save_btn.evaluate("e => e.outerHTML"))
    print("Exit btn:", exit_btn.evaluate("e => e.outerHTML"))
