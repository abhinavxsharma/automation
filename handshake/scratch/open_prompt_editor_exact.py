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
    dismiss_timer(page)

    # Find the prompt heading
    h = page.locator("text='Enter your prompt:'").first
    print("Prompt heading visible:", h.is_visible())
    h.scroll_into_view_if_needed()
    time.sleep(0.5)

    # Find the edit button inside or right after this section
    # Let's inspect all 'Edit this step' buttons and check their bounding box relative to 'Enter your prompt:'
    h_box = h.bounding_box()
    print("Heading box:", h_box)

    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print(f"Total edit buttons: {len(edit_btns)}")
    target_btn = None
    min_dist = float("inf")
    for b in edit_btns:
        b_box = b.bounding_box()
        if b_box and b_box["y"] > h_box["y"] and (b_box["y"] - h_box["y"]) < 600:
            print(
                f"Found button below heading at y={b_box['y']} (dist={b_box['y'] - h_box['y']})"
            )
            target_btn = b
            break

    if target_btn:
        print("Clicking target edit button...")
        target_btn.click(force=True)
        time.sleep(2)
        dismiss_timer(page)
        page.screenshot(path="handshake/scratch/prompt_editor_opened.png")
        print("Saved prompt_editor_opened.png")

        ta = page.locator("textarea").first
        print("Textarea visible now:", ta.is_visible())
        if ta.is_visible():
            print("Current prompt value:\n", ta.input_value()[:100])
    else:
        print("No target button found!")
