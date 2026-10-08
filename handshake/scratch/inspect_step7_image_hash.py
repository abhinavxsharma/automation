import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Let's inspect step 7's view mode
    # What does the image tag show right now?
    img_tags = page.locator("div.flex-col:has-text('Enter your prompt') img, section:has-text('Enter your prompt') img").all()
    print(f"Found {len(img_tags)} img tags near prompt.")
    for i, im in enumerate(img_tags):
        src = im.get_attribute("src") or ""
        print(f"  Img {i}: src_len={len(src)} src_prefix={src[:80]}")

    # Also check all images on page
    all_imgs = page.locator("img").all()
    print(f"\nTotal img tags on page: {len(all_imgs)}")
    for i, im in enumerate(all_imgs):
        src = im.get_attribute("src") or ""
        alt = im.get_attribute("alt") or ""
        aria = im.get_attribute("aria-label") or ""
        print(f"  All-Img {i}: alt='{alt}' aria='{aria}' src_prefix={src[:80]}")

    # Check button[aria-label*='View file']
    file_btns = page.locator("button[aria-label*='View file']").all()
    print(f"\nFound {len(file_btns)} View file buttons:")
    for b in file_btns:
        print("  File btn:", b.get_attribute("aria-label"))
