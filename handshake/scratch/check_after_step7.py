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
                time.sleep(1.0)
    except Exception:
        pass


def main():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        page.wait_for_selector("text=Computer Systems", timeout=15000)
        dismiss_timer(page)

        page.screenshot(path="handshake/scratch/current_after_submitting.png")
        print("Saved current_after_submitting.png")

        # Check for dialogs
        dialogs = page.locator("div[role='dialog']").all()
        print("Dialogs:", len(dialogs))
        for d in dialogs:
            print("Dialog text:", d.inner_text())

        # Check Step 7 textarea
        ta = page.locator("textarea")
        print("Textareas visible:", [ta.nth(i).is_visible() for i in range(ta.count())])

        # Check if checkboxes appeared
        cbs = page.locator("input[type='checkbox'], [role='checkbox']").all()
        print("Checkboxes count:", len(cbs))


if __name__ == "__main__":
    main()
