import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.append(str(Path(__file__).parent))
from chrome_helper import get_task_page


def dismiss_timer(page):
    try:
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible(timeout=1000):
            box = st.bounding_box()
            if box:
                print("Clicking Start timer...")
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                time.sleep(1.0)
    except Exception:
        pass


def main():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        page.wait_for_selector("text=Computer Systems", timeout=15000)
        dismiss_timer(page)

        edit_btns = page.locator("button[aria-label='Edit this step']").all()
        step7_btn = edit_btns[7]
        step7_btn.scroll_into_view_if_needed()
        time.sleep(1.0)
        dismiss_timer(page)

        print("Clicking Step 7 edit button...")
        step7_btn.click(force=True)
        time.sleep(2.0)
        dismiss_timer(page)

        page.screenshot(path="handshake/scratch/step7_opened_now.png")
        print("Saved step7_opened_now.png")

        ta = page.locator("textarea").first
        if ta.is_visible():
            print("Current textarea value in Step 7:\n", repr(ta.input_value()))

        imgs = page.locator("img[src*='storage.googleapis.com'], img[src*='blob']").all()
        print(f"Images in Step 7 editor: {len(imgs)}")
        for im in imgs:
            print(" -", im.get_attribute("src")[:80])


if __name__ == "__main__":
    main()
