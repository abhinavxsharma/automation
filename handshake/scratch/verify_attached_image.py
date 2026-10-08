import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Check View file / Download buttons
    file_btns = page.locator("button[aria-label*='View file'], button[aria-label*='download' i], button:has(svg)").all()
    for b in file_btns:
        aria = b.get_attribute("aria-label") or ""
        txt = b.inner_text().strip()
        if "file" in aria.lower() or "dag" in aria.lower() or "diagram" in aria.lower() or "image" in aria.lower():
            print(f"File button found: aria='{aria}' text='{txt}'")

    # Check all img tags
    imgs = page.locator("img").all()
    for i, im in enumerate(imgs):
        src = im.get_attribute("src") or ""
        alt = im.get_attribute("alt") or ""
        if "storage.googleapis" in src or "blob:" in src or "data:image" in src:
            print(f"Target img [{i}]: alt='{alt}' src='{src[:100]}...'")
            im.screenshot(path=f"scratch/actual_uploaded_thumbnail.png")
            print("Thumbnail saved to scratch/actual_uploaded_thumbnail.png")
