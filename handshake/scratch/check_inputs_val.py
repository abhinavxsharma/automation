import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    for ta in pg.locator("textarea").all():
        print("Textarea value:", repr(ta.input_value()[:100]))

    imgs = pg.locator("img").all()
    print("Images count:", len(imgs))
    for im in imgs:
        if im.is_visible():
            print("Visible img src:", im.get_attribute("src")[:80])
