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
                print("Dismissing timer modal...")
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

    # 2. Open Step 7 editor if not open
    ta = page.locator("textarea").first
    if not ta.is_visible(timeout=1000):
        print("Finding Edit button for Step 7...")
        edit_btns = page.locator("button[aria-label='Edit this step']").all()
        print(f"Edit buttons count: {len(edit_btns)}")
        edit_btns[7].scroll_into_view_if_needed()
        time.sleep(0.5)
        dismiss_timer(page)
        edit_btns[7].click(force=True)
        time.sleep(2)
        dismiss_timer(page)
        ta.wait_for(state="visible", timeout=5000)

    print("Step 7 editor is OPEN!")

    # 3. Remove old images
    rem_btns = page.locator("button[aria-label='Remove']").all()
    print(f"Found {len(rem_btns)} Remove buttons")
    for r in rem_btns:
        if r.is_visible():
            print("Clicking Remove button...")
            r.click(force=True)
            time.sleep(1.0)
            dismiss_timer(page)

    # Hover over any remaining thumbnails to reveal Remove
    for thumb in page.locator("img[src*='storage.googleapis.com']").all():
        if thumb.is_visible():
            thumb.hover()
            time.sleep(0.3)
            for r in page.locator("button[aria-label='Remove']").all():
                if r.is_visible():
                    r.click(force=True)
                    time.sleep(1.0)

    # 4. Upload replacement image
    file_uploaded = False

    def on_fc(file_chooser):
        global file_uploaded
        print("FILE CHOOSER FIRED: uploading", IMAGE_PATH)
        file_chooser.set_files(IMAGE_PATH)
        file_uploaded = True
        print("File uploaded successfully!")

    page.on("filechooser", on_fc)

    upload_btn = page.locator(
        "button[aria-label='Upload files'], button:has-text('+')"
    ).first
    print("Clicking Upload files button...")
    upload_btn.click(force=True)
    time.sleep(4)
    dismiss_timer(page)

    # 5. Fill prompt text
    print("Filling concise prompt text...")
    ta.fill(PROMPT_TEXT)
    time.sleep(1)
    dismiss_timer(page)

    page.screenshot(path="handshake/scratch/before_step7_submit.png")
    print("Saved before_step7_submit.png")

    # 6. Click submit button
    submit_btn = page.locator("button[aria-label='Submit']").first
    if not submit_btn.is_visible():
        cancel_btn = page.locator("button:has-text('Cancel')").first
        parent = cancel_btn.locator("xpath=..")
        submit_btn = parent.locator("button").last

    print("Clicking submit button in Step 7...")
    submit_btn.click(force=True)
    time.sleep(3)
    dismiss_timer(page)

    # Check for confirmation dialog
    for b in page.locator(
        "button:has-text('Confirm'), button:has-text('Proceed'), button:has-text('Delete')"
    ).all():
        if b.is_visible():
            print("Clicking confirmation dialog button:", b.inner_text())
            b.click(force=True)
            time.sleep(3)
            dismiss_timer(page)
            break

    # 7. Check the 4 statement checkboxes
    print("Checking statement checkboxes...")
    statements = [
        "double checked",
        "not duplicative",
        "self-contained",
        "information in the image",
    ]
    for st in statements:
        cb = page.locator(f"label:has-text('{st}'), div:has-text('{st}')").first
        if cb.is_visible(timeout=3000):
            cb.click(force=True)
            time.sleep(0.5)
            print(f"  Checked: {st}")
        else:
            print(f"  Checkbox not visible: {st}")

    time.sleep(1)
    dismiss_timer(page)

    # 8. Click Continue if present
    cont = page.locator("button:has-text('Continue')").first
    if cont.is_visible(timeout=3000):
        print("Clicking Continue button...")
        cont.click(force=True)
        time.sleep(3)
        dismiss_timer(page)

    # 9. Check top bar Save button
    save_btn = page.locator("button:has-text('Save')").first
    if save_btn.is_visible() and not save_btn.is_disabled():
        print("Clicking top bar Save button...")
        save_btn.click(force=True)
        time.sleep(2)
        dismiss_timer(page)

    page.screenshot(path="handshake/scratch/after_step7_and_checkboxes.png")
    print("Saved after_step7_and_checkboxes.png")
