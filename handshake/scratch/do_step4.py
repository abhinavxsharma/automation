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
            time.sleep(0.5)


with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)
    dismiss_timer(pg)

    active_block = pg.locator("div[data-block-id]").last

    # 1. Upload diagram
    upload_btn = active_block.locator("button[aria-label='Upload files']").first
    print("Uploading diagram:", diagram_path)
    with pg.expect_file_chooser() as fc_info:
        upload_btn.click(force=True)
    fc_info.value.set_files(diagram_path)
    print("Diagram passed to file chooser. Waiting 4s for thumbnail...")
    time.sleep(4)

    dismiss_timer(pg)

    # 2. Verify image thumbnail is attached
    imgs = active_block.locator("img").all()
    print("Attached images count in block:", len(imgs))
    for im in imgs:
        print("  Img src:", im.get_attribute("src")[:80])

    # 3. Fill prompt into textarea
    ta = active_block.locator("textarea").first
    print(f"Filling prompt ({len(prompt_text)} chars)...")
    ta.fill(prompt_text)
    time.sleep(2)
    print("Prompt filled. Value len:", len(ta.input_value()))

    dismiss_timer(pg)

    # 4. Click Continue on the active block
    cont = active_block.locator('button[aria-label="Continue"], button:has-text("Continue")').first
    print("Clicking Continue on active block...")
    cont.click(force=True)
    time.sleep(4)

    dismiss_timer(pg)

    # 5. Check if statement checkboxes appeared
    print("\n--- Checkboxes / Labels ---")
    statements = [
        "double checked",
        "not duplicative",
        "self-contained",
        "information in the image"
    ]
    for st in statements:
        cb = pg.locator(f"label:has-text('{st}'), div:has-text('{st}')").first
        if cb.is_visible():
            print(f"  Found statement: {st} (clicking...)")
            cb.click(force=True)
            time.sleep(0.5)

    pg.screenshot(path="scratch/step4_complete_result.png")
    print("Saved scratch/step4_complete_result.png")

    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    print("\nBody lines:")
    for ln in lines[-35:]:
        print(" ", ln)
