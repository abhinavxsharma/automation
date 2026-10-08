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
                print("Dismissing timer modal...")
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
        print("Total edit buttons:", len(edit_btns))
        step7_btn = edit_btns[7]

        step7_btn.scroll_into_view_if_needed()
        time.sleep(1.0)
        dismiss_timer(page)

        print("Clicking step 7 edit button with force=True...")
        step7_btn.click(force=True)
        time.sleep(2.0)
        dismiss_timer(page)

        ta = page.locator("textarea")
        print("Textarea count:", ta.count())
        if ta.count() > 0:
            print("Textarea visible:", ta.first.is_visible())
            print("Value:", repr(ta.first.input_value()[:60]))

        page.screenshot(path="handshake/scratch/editor_check.png")
        print("Saved editor_check.png")


if __name__ == "__main__":
    main()
