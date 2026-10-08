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

        # Inspect all buttons in Step 7 editor
        ta = page.locator("textarea").first
        card = ta.locator("xpath=ancestor::div[contains(@class, 'card') or contains(@class, 'Card') or contains(@class, 'border') or contains(@class, 'rounded')][4]")
        print("Card inner text summary:")
        print(card.inner_text()[:300])

        btns = card.locator("button").all()
        print(f"\nButtons in Step 7 editor card ({len(btns)}):")
        for i, b in enumerate(btns):
            print(f"Btn {i}: text={repr(b.inner_text())}, aria-label={repr(b.get_attribute('aria-label'))}, title={repr(b.get_attribute('title'))}, disabled={b.is_disabled()}, type={repr(b.get_attribute('type'))}")


if __name__ == "__main__":
    main()
