import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    btns = pg.locator("button, a").all()
    for btn in btns:
        try:
            txt = btn.inner_text().strip()
            if txt in ["Save", "Exit", "Exit task"]:
                print(f"Button: text='{txt}', tag={btn.evaluate('e => e.tagName')}, html={btn.evaluate('e => e.outerHTML')}")
        except Exception as e:
            pass
