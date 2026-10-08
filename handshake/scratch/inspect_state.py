import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(2)
    print("URL:", pg.url)
    print("Title:", pg.title())
    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    print("Body lines:")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    for ln in lines[-30:]:
        print(" ", ln)
