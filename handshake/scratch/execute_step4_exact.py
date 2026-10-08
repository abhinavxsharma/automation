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

    # 1. Remove old image if any
    rem = active_block.locator("button[aria-label='Remove']").first
    if rem.is_visible():
        rem.click(force=True)
        time.sleep(1)

    # 2. Upload diagram
    upload_btn = active_block.locator("button[aria-label='Upload files']").first
    if upload_btn.is_visible():
        print("Uploading diagram:", diagram_path)
        with pg.expect_file_chooser() as fc_info:
            upload_btn.click(force=True)
        fc_info.value.set_files(diagram_path)
        print("Diagram passed to file chooser. Waiting 3s...")
        time.sleep(3)

    dismiss_timer(pg)

    # 3. Fill prompt into textarea
    ta = active_block.locator("textarea").first
    print(f"Filling prompt ({len(prompt_text)} chars)...")
    ta.fill(prompt_text)
    time.sleep(1)

    dismiss_timer(pg)

    # 4. Click Submit (up-arrow button)
    submit_btn = active_block.locator("button[aria-label='Submit']").first
    print("Submit button visible?", submit_btn.is_visible())
    if not submit_btn.is_visible():
        # try any submit button in page
        submit_btn = pg.locator("button[aria-label='Submit']").first
    if submit_btn.is_visible():
        print("Clicking Submit (up-arrow) button...")
        submit_btn.click(force=True)
        time.sleep(3)

    dismiss_timer(pg)

    # 5. Check if statement checkboxes appear
    print("Checking statement checkboxes...")
    statements = [
        "double checked",
        "not duplicative",
        "self-contained",
        "information in the image",
    ]
    for st in statements:
        cb = pg.locator(f"label:has-text('{st}'), div:has-text('{st}')").first
        if cb.is_visible(timeout=3000):
            cb.click(force=True)
            print(f"  Checked: {st}")
            time.sleep(0.3)

    time.sleep(1)
    dismiss_timer(pg)

    # 6. Click Continue
    cont = pg.locator("button:has-text('Continue')").last
    print("Continue button visible?", cont.is_visible(), "Enabled?", cont.is_enabled())
    if cont.is_visible():
        print("Clicking Continue...")
        cont.click(force=True)
        time.sleep(5)

    dismiss_timer(pg)
    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    print("\nBody lines:")
    for ln in lines[-35:]:
        print(" ", ln)
    pg.screenshot(path="scratch/step5_after_submit_flow.png")
    print("Saved scratch/step5_after_submit_flow.png")
