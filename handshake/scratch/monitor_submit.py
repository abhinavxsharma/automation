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

    # Listen to console and response
    pg.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}"))
    pg.on("response", lambda resp: print(f"RESP: {resp.status} {resp.url[:70]}") if any(k in resp.url for k in ["graphql", "api", "task", "upload", "block"]) else None)

    active_block = pg.locator("div[data-block-id]").last

    # Upload diagram
    upload_btn = active_block.locator("button[aria-label='Upload files'], button:has-text('+')").first
    if not upload_btn.is_visible():
        upload_btn = active_block.locator("button").filter(has=pg.locator("svg")).nth(1)
    print("Upload btn found:", upload_btn.is_visible())

    with pg.expect_file_chooser() as fc_info:
        upload_btn.click(force=True)
    fc_info.value.set_files(diagram_path)
    print("Files set. Waiting 5s for upload network completion...")
    time.sleep(5)

    dismiss_timer(pg)

    # Fill prompt
    ta = active_block.locator("textarea").first
    print("Filling prompt...")
    ta.fill(prompt_text)
    time.sleep(2)

    dismiss_timer(pg)

    # Click Continue
    cont = active_block.locator('button:has-text("Continue")').first
    print("Clicking Continue...")
    cont.click(force=True)
    print("Waiting 10s and observing responses...")
    time.sleep(10)

    dismiss_timer(pg)
    pg.screenshot(path="scratch/step4_after_network_wait.png")
    print("Saved scratch/step4_after_network_wait.png")
