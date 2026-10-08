import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.append(str(Path(__file__).parent))
from chrome_helper import get_task_page


def dismiss_timer(page):
    try:
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible(timeout=500):
            box = st.bounding_box()
            if box:
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                time.sleep(0.5)
    except Exception:
        pass


def main():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        page.wait_for_selector("text=Computer Systems", timeout=15000)
        dismiss_timer(page)

        # Check if textarea is currently visible
        ta = page.locator("textarea")
        print("Textarea count:", ta.count())
        if ta.count() > 0:
            print("Textarea visible:", ta.first.is_visible())
            if ta.first.is_visible():
                print("Textarea value:", repr(ta.first.input_value()[:100]))
                ta.first.scroll_into_view_if_needed()
                time.sleep(0.5)
                page.screenshot(path="handshake/scratch/textarea_view.png")

        # Check Step 7 edit button
        edit_btns = page.locator("button[aria-label='Edit this step']").all()
        print("Total edit buttons:", len(edit_btns))
        if len(edit_btns) > 7:
            print("Step 7 button box:", edit_btns[7].bounding_box())


if __name__ == "__main__":
    main()
