import json
import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with open("workspace/v2/artifacts.json", "r", encoding="utf-8") as f:
    artifacts = json.load(f)

prompt_text = artifacts["prompt"]


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

    # 1. Fill prompt into textarea
    ta = pg.locator("textarea").first
    print("Filling prompt into textarea...")
    ta.fill(prompt_text, force=True)
    time.sleep(1)
    print("Filled prompt. Length:", len(ta.input_value()))

    dismiss_timer(pg)

    # 2. Click Continue
    cont = pg.locator('button[aria-label="Continue"], button:has-text("Continue")').first
    print("Clicking Continue...")
    cont.click(force=True)
    time.sleep(3)

    dismiss_timer(pg)

    # 3. Check for checkboxes
    print("\n--- Checkboxes / Labels ---")
    cbs = pg.locator('input[type="checkbox"], [role="checkbox"], label').all()
    for cb in cbs:
        if cb.is_visible():
            t = cb.inner_text().strip()
            if t:
                print("  CB:", repr(t[:100]))

    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    print("\nBody lines:")
    for ln in lines[-35:]:
        print(" ", ln)
    pg.screenshot(path="scratch/step4_after_prompt_fill.png")
    print("Saved scratch/step4_after_prompt_fill.png")
