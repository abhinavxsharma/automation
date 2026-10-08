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

        # Find all edit buttons and texts
        edit_btns = page.locator("button[aria-label='Edit this step']").all()
        print(f"Total edit buttons: {len(edit_btns)}")
        for i, b in enumerate(edit_btns):
            t = b.evaluate("""
                el => {
                    let cur = el.parentElement;
                    while (cur && (!cur.innerText || cur.innerText.trim().length < 15) && cur !== document.body) {
                        cur = cur.parentElement;
                    }
                    return cur ? cur.innerText.substring(0, 120).replace(/\\n/g, ' ') : 'EMPTY';
                }
            """)
            print(f"Btn {i}: {t}")

        # Scroll to Step 7
        if len(edit_btns) > 7:
            edit_btns[7].scroll_into_view_if_needed()
            time.sleep(1.0)
            page.screenshot(path="handshake/scratch/step7_scrolled.png")
            print("Saved step7_scrolled.png")

        # Scroll further down
        if len(edit_btns) > 8:
            edit_btns[-1].scroll_into_view_if_needed()
            time.sleep(1.0)
            page.screenshot(path="handshake/scratch/step_last_scrolled.png")
            print("Saved step_last_scrolled.png")


if __name__ == "__main__":
    main()
