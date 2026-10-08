import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    dialogs = pg.locator("[role='dialog'], [role='alertdialog']").all()
    print("Dialogs:", len(dialogs))
    for d in dialogs:
        print("--- DIALOG TEXT ---")
        print(d.inner_text())
        print("-------------------")
    pg.screenshot(path="scratch/current_dialog_modal.png")
