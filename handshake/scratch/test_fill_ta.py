import json
import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with open("workspace/v2/artifacts.json", "r", encoding="utf-8") as f:
    artifacts = json.load(f)

prompt_text = artifacts["prompt"]

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    ta = pg.locator("textarea").first
    print("Ta visible?", ta.is_visible())
    ta.click()
    time.sleep(0.5)
    ta.fill(prompt_text)
    time.sleep(1)
    print("Ta value length after fill:", len(ta.input_value()))

    # Also verify if file is attached
    file_previews = pg.locator("div[data-block-id] img, div[data-block-id] [role='img']").all()
    print("File preview count in block:", len(file_previews))
