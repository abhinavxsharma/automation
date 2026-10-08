import urllib.request, base64
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Find the image in Step 7 or on page
    imgs = page.locator("img").all()
    print(f"Total img tags on page: {len(imgs)}")
    for i, img in enumerate(imgs):
        src = img.get_attribute("src") or ""
        alt = img.get_attribute("alt") or ""
        print(f"[{i}] alt='{alt}' src_len={len(src)} src_prefix='{src[:60]}'")
        if "data:image" in src:
            header, encoded = src.split(",", 1)
            data = base64.b64decode(encoded)
            with open(f"scratch/uploaded_img_{i}.png", "wb") as f:
                f.write(data)
            print(f"Saved data URL image to scratch/uploaded_img_{i}.png ({len(data)} bytes)")
        elif src.startswith("http"):
            # Download
            try:
                # We can also capture screenshot of the img element directly!
                img.screenshot(path=f"scratch/uploaded_img_{i}_element.png")
                print(f"Saved element screenshot to scratch/uploaded_img_{i}_element.png")
            except Exception as e:
                print(f"Could not screenshot img {i}: {e}")
