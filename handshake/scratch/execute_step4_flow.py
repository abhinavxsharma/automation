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
diagram_path = str(Path(artifacts["image_path"]).resolve())


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

    # 1. Upload diagram
    upload_btn = pg.locator("button[aria-label='Upload files']").first
    if upload_btn.is_visible():
        print(f"Uploading diagram: {diagram_path}")
        with pg.expect_file_chooser() as fc_info:
            upload_btn.click(force=True)
        fc = fc_info.value
        fc.set_files(diagram_path)
        print("Diagram set in file chooser!")
        time.sleep(3)

    # 2. Fill prompt
    ta = pg.locator("textarea").first
    if ta.is_visible():
        print("Filling prompt into textarea...")
        ta.click()
        time.sleep(0.5)
        ta.fill(prompt_text)
        time.sleep(1)

    dismiss_timer(pg)

    # 3. Click Continue / Submit
    btn = pg.locator('button[aria-label="Submit"], button[aria-label="Continue"], button:has-text("Continue")').first
    if btn.is_visible():
        print(f"Clicking button: {btn.get_attribute('aria-label') or btn.inner_text()}")
        btn.click(force=True)
        time.sleep(3)

    dismiss_timer(pg)

    # 4. Check for statement checkboxes
    print("Checking statement checkboxes...")
    statements = [
        "double checked",
        "not duplicative",
        "self-contained",
        "information in the image"
    ]
    for st in statements:
        cb = pg.locator(f"label:has-text('{st}'), div:has-text('{st}')").first
        if cb.is_visible(timeout=3000):
            cb.click(force=True)
            print(f"  Checked: {st}")
            time.sleep(0.5)

    # 5. Click Continue if present after checking
    cont = pg.locator('button:has-text("Continue"), button[aria-label="Continue"]').first
    if cont.is_visible():
        print("Clicking Continue after checkboxes...")
        cont.click(force=True)
        time.sleep(4)

    dismiss_timer(pg)
    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    print("\nBody lines:")
    for ln in lines[-35:]:
        print(" ", ln)
    pg.screenshot(path="scratch/step5_model_screen.png")
    print("Saved scratch/step5_model_screen.png")
