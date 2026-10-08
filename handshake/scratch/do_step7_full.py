import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.append(str(Path(__file__).parent))
from chrome_helper import get_task_page

IMAGE_PATH = r"C:\Users\Abhinav\Downloads\lab image@2.png"
PROMPT_TEXT = (
    "Determine the output Q as a Boolean function of the independent inputs A, B, and C "
    "from the provided circuit image. Treat the image as authoritative for all gate types "
    "and connections. A wire crossing is connected only when an explicit junction dot is shown. "
    "Give Q in minimal sum-of-products form. Provide the Boolean derivation briefly, then state "
    "the final expression for Q clearly on its own final line."
)


def dismiss_timer(page):
    try:
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible(timeout=500):
            box = st.bounding_box()
            if box:
                print("Dismissing timer modal...")
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                time.sleep(1.0)
    except Exception:
        pass


def main():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        page.wait_for_selector("text=Computer Systems", timeout=15000)
        dismiss_timer(page)

        # 1. Ensure Step 7 editor is open
        ta = page.locator("textarea").first
        if not ta.is_visible():
            print("Step 7 editor not open, clicking edit button...")
            edit_btns = page.locator("button[aria-label='Edit this step']").all()
            edit_btns[7].scroll_into_view_if_needed()
            time.sleep(0.5)
            dismiss_timer(page)
            edit_btns[7].click(force=True)
            time.sleep(2.0)
            dismiss_timer(page)
            ta.wait_for(state="visible", timeout=5000)

        print("Step 7 editor is ready.")
        dismiss_timer(page)

        # 2. Remove old image
        # Let's find any remove button or hover thumbnail
        thumbs = page.locator("img[src*='storage.googleapis.com'], img[src*='blob']").all()
        print(f"Thumbnails found: {len(thumbs)}")
        for thumb in thumbs:
            try:
                thumb.hover()
                time.sleep(0.5)
            except Exception:
                pass

        rem_btns = page.locator("button[aria-label='Remove']").all()
        print(f"Remove buttons found: {len(rem_btns)}")
        for r in rem_btns:
            if r.is_visible():
                print("Clicking remove button...")
                r.click(force=True)
                time.sleep(1.5)
                dismiss_timer(page)

        # 3. Setup file chooser listener
        fc_fired = [False]

        def on_fc(file_chooser):
            print("FILE CHOOSER FIRED! Setting file:", IMAGE_PATH)
            file_chooser.set_files(IMAGE_PATH)
            fc_fired[0] = True
            print("File set successfully!")

        page.on("filechooser", on_fc)

        # 4. Click Upload files (+) button
        upload_btn = page.locator("button[aria-label='Upload files'], button:has-text('+')").first
        print("Clicking upload button...")
        upload_btn.click(force=True)
        time.sleep(4.0)
        dismiss_timer(page)
        print("File chooser fired status:", fc_fired[0])

        # 5. Fill prompt text
        print("Filling concise prompt text...")
        ta.fill(PROMPT_TEXT)
        time.sleep(1.0)
        dismiss_timer(page)

        page.screenshot(path="handshake/scratch/before_step7_submit.png")
        print("Saved before_step7_submit.png")

        # 6. Click Step 7 submit button
        cancel_btn = page.locator("button:has-text('Cancel')").first
        parent = cancel_btn.locator("xpath=..")
        submit_btn = parent.locator("button").last
        print("Clicking Step 7 submit arrow button...")
        submit_btn.click(force=True)
        time.sleep(3.0)
        dismiss_timer(page)

        # Check for confirmation dialog
        for b in page.locator("button:has-text('Confirm'), button:has-text('Proceed'), button:has-text('Delete')").all():
            if b.is_visible():
                print("Clicking confirmation dialog button:", b.inner_text())
                b.click(force=True)
                time.sleep(3.0)
                dismiss_timer(page)
                break

        page.screenshot(path="handshake/scratch/after_step7_submitted.png")
        print("Saved after_step7_submitted.png")


if __name__ == "__main__":
    main()
