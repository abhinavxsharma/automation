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

        edit_btns = page.locator("button[aria-label='Edit this step']").all()
        print(f"Total edit buttons: {len(edit_btns)}")
        step7_btn = edit_btns[7]
        step7_btn.scroll_into_view_if_needed()
        time.sleep(0.5)
        dismiss_timer(page)

        print("Clicking Step 7 edit button...")
        step7_btn.click(force=True)
        time.sleep(1.5)
        dismiss_timer(page)

        # Wait for textarea
        ta = page.locator("textarea").first
        ta.wait_for(state="visible", timeout=5000)
        print("Textarea is now visible!")
        print("Textarea current value:", repr(ta.input_value()))

        # Check for thumbnails/images in editor
        editor_card = ta.locator("xpath=ancestor::div[contains(@class, 'card') or contains(@class, 'Card') or contains(@class, 'border')][1]")
        imgs = page.locator("img[src*='storage.googleapis.com'], img[src*='blob']").all()
        print(f"Images in editor / page: {len(imgs)}")
        for im in imgs:
            print("Img src:", im.get_attribute("src")[:80])

        # Check for remove buttons
        rem_btns = page.locator("button[aria-label='Remove']").all()
        print(f"Remove buttons: {len(rem_btns)}")

        # Check for upload button
        upload_btn = page.locator("button[aria-label='Upload files'], button:has-text('+')").all()
        print(f"Upload buttons: {len(upload_btn)}")

        page.screenshot(path="handshake/scratch/step7_opened.png")
        print("Saved handshake/scratch/step7_opened.png")


if __name__ == "__main__":
    main()
