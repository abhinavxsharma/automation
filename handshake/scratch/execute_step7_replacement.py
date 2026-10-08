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

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Wait for page hydration
    page.wait_for_selector("text=Computer Systems", timeout=15000)

    # 1. Dismiss timer if visible
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible(timeout=1500):
        print("Dismissing Start timer...")
        st.click(force=True)
        page.wait_for_timeout(1000)

    # 2. Check if Step 7 editor is open
    ta = page.locator("textarea").first
    if not ta.is_visible(timeout=1000):
        print("Opening Step 7 editor...")
        edit_btns = page.locator("button[aria-label='Edit this step']").all()
        print("Found edit buttons:", len(edit_btns))
        if len(edit_btns) > 7:
            edit_btns[7].scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            edit_btns[7].click(force=True)
            page.wait_for_timeout(1500)
            ta.wait_for(state="visible", timeout=5000)
        else:
            raise RuntimeError(f"Expected at least 8 edit buttons, found {len(edit_btns)}")

    print("Step 7 editor is active!")

    # 3. Remove old image if present
    rem_btn = page.locator("button[aria-label='Remove']").first
    if rem_btn.is_visible(timeout=1500):
        print("Removing old image...")
        rem_btn.click(force=True)
        page.wait_for_timeout(1500)
    else:
        print("No old image remove button visible (maybe already removed)")

    # 4. Upload new image
    print(f"Uploading replacement image from: {IMAGE_PATH}")
    upload_btn = page.locator(
        "button[aria-label='Upload files'], button:has-text('+')"
    ).first
    with page.expect_file_chooser() as fc_info:
        upload_btn.click(force=True)
    fc = fc_info.value
    fc.set_files(IMAGE_PATH)
    page.wait_for_timeout(3000)

    # 5. Set new concise prompt
    print("Setting new concise prompt...")
    ta.fill(PROMPT_TEXT)
    page.wait_for_timeout(500)

    # Take screenshot before submitting
    page.screenshot(path="handshake/scratch/step7_ready_to_submit.png")
    print("Saved step7_ready_to_submit.png")

    # 6. Click submit (up-arrow button next to Cancel)
    cancel_btn = page.locator("button:has-text('Cancel')").first
    parent = cancel_btn.locator("xpath=..")
    arrow_btn = parent.locator("button").last
    print("Submitting Step 7 card...")
    arrow_btn.click(force=True)
    page.wait_for_timeout(2000)

    # 7. Check if confirmation dialog appears
    confirm_btn = page.locator(
        "button:has-text('Confirm'), button:has-text('Continue'), button:has-text('Delete'), button:has-text('Proceed')"
    ).all()
    for b in confirm_btn:
        if b.is_visible():
            print("Clicking confirmation button:", b.inner_text())
            b.click(force=True)
            page.wait_for_timeout(2000)
            break

    page.screenshot(path="handshake/scratch/after_step7_submitted.png")
    print("Saved after_step7_submitted.png")
