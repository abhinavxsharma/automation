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

        # Find all edit buttons
        edit_btns = page.locator("button[aria-label='Edit this step']").all()
        print("Total edit buttons:", len(edit_btns))
        for i, b in enumerate(edit_btns):
            box = b.bounding_box()
            vis = b.is_visible()
            print(f"Edit btn {i}: visible={vis}, box={box}")

        # Btn 7 is the one for the prompt and image!
        # Let's scroll it into view and click it!
        step7_btn = edit_btns[7]
        step7_btn.scroll_into_view_if_needed()
        time.sleep(0.5)
        box = step7_btn.bounding_box()
        print(f"Step 7 button after scroll: {box}")

        # Click it
        print("Clicking step 7 edit button...")
        step7_btn.click()
        time.sleep(2.0)

        # Check if textarea appeared
        ta = page.locator("textarea")
        print("Textarea count:", ta.count())
        if ta.count() > 0:
            print("Textarea visible:", ta.first.is_visible())

        page.screenshot(path="handshake/scratch/step7_opened_clean.png")
        print("Saved step7_opened_clean.png")


if __name__ == "__main__":
    main()
