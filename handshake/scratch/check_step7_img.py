import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button[aria-label='Edit this step']", timeout=10000)
    btns = page.locator("button[aria-label='Edit this step']").all()
    print("Found btns:", len(btns))
    if len(btns) > 7:
        btns[7].scroll_into_view_if_needed()
        page.wait_for_timeout(1000)
        page.screenshot(path="scratch/step7_scrolled.png")
        
        imgs = page.locator("img").all()
        print("Images after scroll:", len(imgs))
        for i, img in enumerate(imgs):
            print(f"  Img {i}: src={img.get_attribute('src')[:80]}")
