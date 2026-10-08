import json
import sys
import time
from pathlib import Path

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with open("workspace/v2/artifacts.json", "r", encoding="utf-8") as f:
    artifacts = json.load(f)

image_path = str(Path(artifacts["image_path"]).resolve())
print("Image to upload:", image_path, "Exists:", Path(image_path).exists())

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    upload_btn = pg.locator('button[aria-label="Upload files"]').first
    print("Upload button visible?", upload_btn.is_visible())
    if upload_btn.is_visible():
        with pg.expect_file_chooser() as fc_info:
            upload_btn.click()
        fc = fc_info.value
        fc.set_files(image_path)
        print("Set files called on file chooser!")
        time.sleep(4)

    # Check for preview or attached file elements
    block = pg.locator("div[data-block-id]").last
    html = block.evaluate("el => el.outerHTML")
    print("Block HTML snippet with img/file:")
    for line in html.splitlines():
        if any(w in line for w in ["img", "png", "diagram", "Upload", "file"]):
            print(" ", line[:120])

    pg.screenshot(path="scratch/step4_after_upload.png")
    print("Saved scratch/step4_after_upload.png")
