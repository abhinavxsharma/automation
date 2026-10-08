import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.append(str(Path(__file__).parent))
from chrome_helper import get_task_page


def main():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        page.wait_for_selector("text=Computer Systems", timeout=15000)

        edit_btns = page.locator("button[aria-label='Edit this step']").all()
        print("Total edit buttons:", len(edit_btns))
        btn = edit_btns[7]

        # Let's inspect the button and its container
        btn.scroll_into_view_if_needed()
        time.sleep(1.0)
        box = btn.bounding_box()
        print(f"Step 7 edit button bounding box: {box}")

        page.screenshot(path="handshake/scratch/btn7_in_view.png")

        # Let's click it using mouse coordinates directly to be 100% sure!
        if box:
            print("Clicking at center of box:", box["x"] + box["width"]/2, box["y"] + box["height"]/2)
            page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
        else:
            print("Clicking via playwright locator click...")
            btn.click(force=True)

        time.sleep(2.0)
        page.screenshot(path="handshake/scratch/after_btn7_click.png")

        # Check if textarea appeared
        ta = page.locator("textarea")
        print("Textarea count:", ta.count())
        if ta.count() > 0:
            print("Textarea visible:", ta.first.is_visible())


if __name__ == "__main__":
    main()
