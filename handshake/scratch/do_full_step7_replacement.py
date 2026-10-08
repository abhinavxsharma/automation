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
    except Exception:
        pass


with sync_playwright() as p:
    browser, page = get_task_page(p)

    # 1. Wait for hydration
    page.wait_for_selector("text=Computer Systems", timeout=15000)
    dismiss_timer(page)

    # 2. Locate Step 7 edit button
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print(f"Total edit buttons found: {len(edit_btns)}")
    btn7 = edit_btns[7]
    btn7.scroll_into_view_if_needed()
    time.sleep(0.5)
    dismiss_timer(page)

    # 3. Open Step 7 editor
    print("Clicking Edit on Step 7...")
    btn7.click(force=True)
    time.sleep(2)
    dismiss_timer(page)

    ta = page.locator("textarea").first
    ta.wait_for(state="visible", timeout=5000)
    print("Step 7 editor is open!")

    # 4. Remove all currently attached images
    # Hover over thumbnail area to reveal Remove button
    thumbnails = page.locator("img[src*='storage.googleapis.com']").all()
    print(f"Found {len(thumbnails)} storage images")
    for thumb in thumbnails:
        if thumb.is_visible():
            thumb.hover()
            time.sleep(0.3)
            rem = page.locator("button[aria-label='Remove']").all()
            for r in rem:
                if r.is_visible():
                    print("Clicking Remove button on thumbnail...")
                    r.click(force=True)
                    time.sleep(1.0)
                    break

    # If any Remove button is still present (even hidden), click it
    rem = page.locator("button[aria-label='Remove']").all()
    for r in rem:
        try:
            print("Force-clicking remaining Remove button...")
            r.click(force=True)
            time.sleep(1.0)
        except Exception:
            pass

    page.screenshot(path="handshake/scratch/step7_after_remove_all.png")
    print("Saved step7_after_remove_all.png")

    # 5. Upload new image
    file_uploaded = False

    def on_fc(file_chooser):
        global file_uploaded
        print("FILE CHOOSER FIRED: uploading", IMAGE_PATH)
        file_chooser.set_files(IMAGE_PATH)
        file_uploaded = True
        print("File passed successfully!")

    page.on("filechooser", on_fc)

    upload_btn = page.locator(
        "button[aria-label='Upload files'], button:has-text('+')"
    ).first
    print("Clicking Upload button...")
    upload_btn.click(force=True)
    time.sleep(4)
    dismiss_timer(page)
    print("Upload completed, status:", file_uploaded)

    # 6. Fill new concise prompt
    print("Filling concise prompt text...")
    ta.fill(PROMPT_TEXT)
    time.sleep(1)
    dismiss_timer(page)

    page.screenshot(path="handshake/scratch/step7_ready_final.png")
    print("Saved step7_ready_final.png")

    # 7. Submit Step 7 card
    cancel_btn = page.locator("button:has-text('Cancel')").first
    parent = cancel_btn.locator("xpath=..")
    arrow_btn = parent.locator("button").last
    print("Submitting Step 7 card via arrow button...")
    arrow_btn.click(force=True)
    time.sleep(2)
    dismiss_timer(page)

    # 8. Handle any confirmation dialog (e.g. downstream blocks deletion)
    confirm_btns = page.locator(
        "button:has-text('Confirm'), button:has-text('Continue'), button:has-text('Delete'), button:has-text('Proceed')"
    ).all()
    print(f"Confirmation buttons visible: {len(confirm_btns)}")
    for b in confirm_btns:
        if b.is_visible():
            txt = b.inner_text()
            print(f"Clicking confirmation button: {txt}")
            b.click(force=True)
            time.sleep(3)
            dismiss_timer(page)
            break

    page.screenshot(path="handshake/scratch/step7_after_final_submit.png")
    print("Saved step7_after_final_submit.png")
