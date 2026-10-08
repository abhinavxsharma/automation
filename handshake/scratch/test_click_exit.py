import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    pg.wait_for_timeout(2000)
    # First click Save to make 100% sure everything is saved
    save_btn = pg.locator("button:has-text('Save')")
    if save_btn.count() > 0:
        save_btn.first.click()
        print("Clicked Save")
        pg.wait_for_timeout(1000)
    
    # Click Exit button
    exit_btn = pg.locator("button.TaskTopNav-module__lMEIEG__transparentSubduedButton:has-text('Exit')")
    if exit_btn.count() > 0:
        print("Found top nav Exit button, clicking...")
        exit_btn.first.click()
        pg.wait_for_timeout(1500)
        pg.screenshot(path="scratch/after_click_exit.png")
        txt = pg.evaluate("() => document.body.innerText")
        print("After click exit text preview:")
        print(txt[:600])
    else:
        print("Exit button not found")
