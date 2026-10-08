import os
import sys
import time

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

PROMPT_TEXT = (
    "Determine the output Q as a Boolean function of the independent inputs A, B, and C "
    "from the provided circuit image. Treat the image as authoritative for all gate types "
    "and connections. A wire crossing is connected only when an explicit junction dot is shown. "
    "Give Q in minimal sum-of-products form. Provide the Boolean derivation briefly, then state "
    "the final expression for Q clearly on its own final line."
)

IMAGE_PATH = r"C:\Users\Abhinav\Downloads\lab image@2.png"


def dismiss_timer(page):
    try:
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible(timeout=500):
            box = st.bounding_box()
            if box:
                print("Dismissing Start timer modal via mouse...")
                page.mouse.click(
                    box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
                )
                time.sleep(0.5)
    except Exception as e:
        pass


with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_selector("text=Computer Systems", timeout=15000)
    dismiss_timer(page)

    # 1. Open Step 7 editor if not open
    ta = page.locator("textarea").first
    if not ta.is_visible(timeout=1000):
        print("Opening Step 7 editor...")
        edit_btns = page.locator("button[aria-label='Edit this step']").all()
        print(f"Total edit buttons: {len(edit_btns)}")
        edit_btns[7].scroll_into_view_if_needed()
        time.sleep(0.5)
        edit_btns[7].click(force=True)
        time.sleep(1.5)
        dismiss_timer(page)
        ta.wait_for(state="visible", timeout=5000)

    print("Step 7 editor is open!")
    dismiss_timer(page)

    # 2. Check for old image remove button
    rem_btn = page.locator("button[aria-label='Remove']").first
    if rem_btn.is_visible(timeout=1000):
        print("Removing old image...")
        rem_btn.click(force=True)
        time.sleep(1.5)
        dismiss_timer(page)
    else:
        print("No old image remove button (already removed)")

    # 3. Setup file chooser listener
    file_uploaded = False

    def on_fc(file_chooser):
        global file_uploaded
        print("FILE CHOOSER EVENT TRIGGERED!")
        file_chooser.set_files(IMAGE_PATH)
        file_uploaded = True
        print("Replacement image passed to file chooser!")

    page.on("filechooser", on_fc)

    # Click Upload files button
    upload_btn = page.locator(
        "button[aria-label='Upload files'], button:has-text('+')"
    ).first
    print("Clicking upload button...")
    upload_btn.click(force=True)
    time.sleep(4)
    dismiss_timer(page)

    print("File uploaded status:", file_uploaded)

    # 4. Fill concise prompt text
    print("Filling concise prompt...")
    ta.fill(PROMPT_TEXT)
    time.sleep(1)
    dismiss_timer(page)

    # Save screenshot of ready state
    page.screenshot(path="handshake/scratch/step7_ready_to_submit.png")
    print("Saved handshake/scratch/step7_ready_to_submit.png")

    # 5. Submit Step 7 card
    cancel_btn = page.locator("button:has-text('Cancel')").first
    parent = cancel_btn.locator("xpath=..")
    arrow_btn = parent.locator("button").last
    print("Clicking submit arrow button in Step 7...")
    arrow_btn.click(force=True)
    time.sleep(2)
    dismiss_timer(page)

    # Check for confirmation modal (about downstream blocks deletion)
    confirm_btns = page.locator(
        "button:has-text('Confirm'), button:has-text('Continue'), button:has-text('Delete'), button:has-text('Proceed')"
    ).all()
    print(f"Confirm buttons found: {len(confirm_btns)}")
    for b in confirm_btns:
        if b.is_visible():
            print("Clicking confirmation button:", b.inner_text())
            b.click(force=True)
            time.sleep(2)
            dismiss_timer(page)
            break

    page.screenshot(path="handshake/scratch/after_step7_submitted.png")
    print("Saved handshake/scratch/after_step7_submitted.png")
