import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright


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

    statements = [
        "double checked",
        "not duplicative",
        "self-contained",
        "information in the image",
    ]
    for st in statements:
        cb = pg.locator(f"label:has-text('{st}'), div:has-text('{st}')").first
        if cb.is_visible():
            print(f"Checking statement: {st}")
            cb.click(force=True)
            time.sleep(0.5)

    dismiss_timer(pg)
    time.sleep(1)

    cont = pg.locator('button:has-text("Continue")').last
    print("Continue button enabled?", cont.is_enabled())
    if cont.is_visible():
        print("Clicking Continue to start model generation...")
        cont.click(force=True)
        time.sleep(5)

    dismiss_timer(pg)
    pg.screenshot(path="scratch/step5_model_generation_started.png")
    print("Saved scratch/step5_model_generation_started.png")

    body = pg.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    print("\nBody lines:")
    for ln in lines[-35:]:
        print(" ", ln)
