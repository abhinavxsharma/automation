import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    block = pg.locator("div[data-block-id]").last
    print("Block buttons:", [b.get_attribute("aria-label") or b.inner_text() for b in block.locator("button").all()])
    print("Block textareas:", len(block.locator("textarea").all()))
    print("Block imgs:", len(block.locator("img").all()))
    for im in block.locator("img").all():
        print("  Img:", im.get_attribute("src")[:60])
    pg.screenshot(path="scratch/current_prompt_block.png")
    print("Saved scratch/current_prompt_block.png")
