import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.append(str(Path(__file__).parent))
from chrome_helper import get_task_page


def dismiss_modal_thoroughly(page):
    for attempt in range(5):
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible(timeout=1000):
            box = st.bounding_box()
            print(f"Attempt {attempt}: modal visible, box: {box}")
            if box:
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                time.sleep(1.0)
        else:
            print(f"Modal is not visible on attempt {attempt}")
            break


def main():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        page.wait_for_selector("text=Computer Systems", timeout=15000)
        dismiss_modal_thoroughly(page)

        page.screenshot(path="handshake/scratch/after_dismiss.png")
        print("Saved after_dismiss.png")

        # Now check textarea
        ta = page.locator("textarea")
        print("Textareas found:", ta.count())
        for i in range(ta.count()):
            print(f"Textarea {i} visible: {ta.nth(i).is_visible()}")

        # Check edit buttons
        edit_btns = page.locator("button[aria-label='Edit this step']").all()
        print("Edit buttons:", len(edit_btns))


if __name__ == "__main__":
    main()
