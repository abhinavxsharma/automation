import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    # Check elements matching text Exit
    exit_loc = pg.get_by_text("Exit", exact=True)
    count = exit_loc.count()
    print("Exact 'Exit' count:", count)
    for i in range(count):
        el = exit_loc.nth(i)
        print(f"  [{i}]: tag={el.evaluate('e => e.tagName')}, box={el.bounding_box()}, visible={el.is_visible()}")
