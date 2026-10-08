import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.append(str(Path(__file__).parent))
from chrome_helper import get_task_page


def dismiss_timer(page):
    try:
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible(timeout=1000):
            box = st.bounding_box()
            if box:
                print("Clicking Start timer...")
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                time.sleep(1.0)
    except Exception:
        pass


def main():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        page.wait_for_selector("text=Computer Systems", timeout=15000)
        dismiss_timer(page)

        # Print all text in the main content
        main_text = page.locator("main, div[class*='container'], body").first.inner_text()
        with open("handshake/scratch/live_body_text.txt", "w", encoding="utf-8") as f:
            f.write(main_text)

        print("Saved live_body_text.txt, length:", len(main_text))

        # Check Step 7 block text
        edit_btns = page.locator("button[aria-label='Edit this step']").all()
        print("Edit buttons:", len(edit_btns))
        if len(edit_btns) > 7:
            step7_card_text = edit_btns[7].evaluate("""
                el => {
                    let cur = el.parentElement;
                    while (cur && (!cur.innerText || cur.innerText.trim().length < 50) && cur !== document.body) {
                        cur = cur.parentElement;
                    }
                    return cur ? cur.innerText : 'NONE';
                }
            """)
            print("Step 7 card text:\n", step7_card_text[:400])

        page.screenshot(path="handshake/scratch/uncovered_view.png")
        print("Saved uncovered_view.png")


if __name__ == "__main__":
    main()
