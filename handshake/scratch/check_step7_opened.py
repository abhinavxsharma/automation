import sys
import time

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright


def dismiss_timer(page):
    try:
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible(timeout=500):
            box = st.bounding_box()
            if box:
                page.mouse.click(
                    box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
                )
                time.sleep(0.5)
    except Exception:
        pass


with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_selector("text=Computer Systems", timeout=15000)
    dismiss_timer(page)

    # Find Step 7
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print("Found edit buttons:", len(edit_btns))
    edit_btns[7].scroll_into_view_if_needed()
    time.sleep(0.5)
    edit_btns[7].click(force=True)
    time.sleep(1.5)
    dismiss_timer(page)

    page.screenshot(path="handshake/scratch/step7_opened_live.png")
    print("Saved step7_opened_live.png")

    # Inspect images / buttons inside editor
    imgs = page.locator("img").all()
    print("Total images on page:", len(imgs))
    for i, im in enumerate(imgs):
        print(
            f"Image {i}: visible={im.is_visible()}, src={im.get_attribute('src')[:80]}"
        )

    ta = page.locator("textarea").first
    print("Textarea visible:", ta.is_visible())
    print("Textarea value:\n", ta.input_value())
