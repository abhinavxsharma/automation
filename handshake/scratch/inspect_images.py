import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    # Check images on page
    imgs = page.locator("img").all()
    print("Total images on page:", len(imgs))
    for i, img in enumerate(imgs):
        src = img.get_attribute("src") or ""
        alt = img.get_attribute("alt") or ""
        box = img.bounding_box()
        print(f"  Img {i}: box={box} src={src[:80]} alt={alt}")
