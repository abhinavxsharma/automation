import json
import sys
import time
from pathlib import Path

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with open("workspace/v2/artifacts.json", "r", encoding="utf-8") as f:
    artifacts = json.load(f)

diagram_path = str(Path(artifacts["image_path"]).resolve())


def dismiss_timer(page):
    st = page.locator('button:has-text("Start timer")').first
    if st.is_visible():
        box = st.bounding_box()
        if box:
            print("Dismissing Start timer modal...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            time.sleep(0.5)


with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)
    dismiss_timer(pg)

    upload_btn = pg.locator("button[aria-label='Upload files']").first
    print("Upload btn:", upload_btn.is_visible())

    # Listen to file chooser event
    def on_file_chooser(file_chooser):
        print("FILE CHOOSER EVENT FIRED!")
        print("Is multiple?", file_chooser.is_multiple)
        file_chooser.set_files(diagram_path)
        print("Files passed to file chooser!")

    pg.on("filechooser", on_file_chooser)

    upload_btn.click()
    print("Clicked upload button, waiting...")
    time.sleep(5)
    dismiss_timer(pg)

    block = pg.locator("div[data-block-id]").last
    print("After upload - block buttons:", [b.get_attribute("aria-label") or b.inner_text() for b in block.locator("button").all()])
    print("After upload - block imgs:", len(block.locator("img").all()))
    for im in block.locator("img").all():
        print("  Img src:", im.get_attribute("src")[:80])

    pg.screenshot(path="scratch/after_upload_test.png")
    print("Saved scratch/after_upload_test.png")
