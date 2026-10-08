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

        dialogs = page.locator("div[role='dialog']").all()
        print(f"Total dialogs: {len(dialogs)}")
        for i, d in enumerate(dialogs):
            print(f"--- Dialog {i} ---")
            print("Visible:", d.is_visible())
            print("Text:\n", d.inner_text())
            btns = d.locator("button").all()
            for b in btns:
                print("Button:", b.inner_text(), "box:", b.bounding_box())


if __name__ == "__main__":
    main()
