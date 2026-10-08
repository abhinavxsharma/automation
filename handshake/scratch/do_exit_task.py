import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    pg.wait_for_timeout(1000)
    exit_task_btn = pg.get_by_role("button", name="Exit task")
    if exit_task_btn.count() > 0:
        print("Clicking 'Exit task'...")
        exit_task_btn.first.click()
        pg.wait_for_timeout(3000)
        pg.screenshot(path="scratch/after_exit_task_clicked.png")
        print("Current URL after exit:", pg.url)
        txt = pg.evaluate("() => document.body ? document.body.innerText : ''")
        print("Page preview after exit:")
        print(txt[:400])
    else:
        print("'Exit task' button not found")
