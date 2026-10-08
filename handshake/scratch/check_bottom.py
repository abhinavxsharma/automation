import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.append(str(Path(__file__).parent))
from chrome_helper import get_task_page


def main():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        page.wait_for_selector("text=Computer Systems", timeout=15000)

        # Scroll to bottom of main area
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        page.screenshot(path="handshake/scratch/bottom_page.png")

        # Let's inspect all text elements from the bottom
        edit_btns = page.locator("button[aria-label*='Edit']").all()
        print(f"Total edit buttons after scroll: {len(edit_btns)}")
        for i, btn in enumerate(edit_btns):
            box = btn.bounding_box()
            print(f"Btn {i} box: {box}")

        # Let's check buttons that say 'Continue', 'Submit', 'Next', etc.
        action_btns = page.locator("button").all()
        for b in action_btns:
            if b.is_visible():
                txt = b.inner_text().strip()
                if any(w in txt.lower() for w in ["continue", "submit", "save", "next", "generate", "start"]):
                    print("Action button:", txt, "box:", b.bounding_box())


if __name__ == "__main__":
    main()
