import json
import sys
import time
from pathlib import Path

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with open("workspace/v2/artifacts.json", "r", encoding="utf-8") as f:
    artifacts = json.load(f)

prompt_text = artifacts["prompt"]
image_path = str(Path(artifacts["image_path"]).resolve())


def dismiss_timer(page):
    st = page.locator('button:has-text("Start timer")').first
    if st.is_visible():
        box = st.bounding_box()
        if box:
            print("Dismissing Start timer modal...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            time.sleep(1)


with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)
    dismiss_timer(pg)

    # 1. Upload file
    upload_btn = pg.locator('button[aria-label="Upload files"]').first
    if upload_btn.is_visible():
        print(f"Triggering file upload for: {image_path}")
        with pg.expect_file_chooser() as fc_info:
            upload_btn.click()
        fc = fc_info.value
        fc.set_files(image_path)
        print("File set in file chooser!")
        time.sleep(3)

    # 2. Fill prompt
    ta = pg.locator("textarea").first
    if ta.is_visible():
        print(f"Filling prompt ({len(prompt_text)} chars)...")
        ta.fill(prompt_text)
        time.sleep(2)

    dismiss_timer(pg)

    # 3. Check for checkboxes or uploaded image preview
    print("\n--- Checkboxes / Labels ---")
    for cb in pg.locator('input[type="checkbox"], [role="checkbox"], label').all():
        if cb.is_visible():
            t = cb.inner_text().strip()
            if t:
                print("  CB:", repr(t[:80]))

    # 4. Check buttons
    print("\n--- Buttons ---")
    for b in pg.locator("div[data-block-id] button").all():
        if b.is_visible():
            print("  Btn:", repr(b.inner_text()))

    pg.screenshot(path="scratch/step4_filled.png")
    print("Saved scratch/step4_filled.png")
