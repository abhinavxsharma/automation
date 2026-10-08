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
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                time.sleep(1.0)
    except Exception:
        pass


def main():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        page.wait_for_selector("text=Computer Systems", timeout=15000)
        dismiss_timer(page)

        # 1. Check if Step 7 editor is open
        ta = page.locator("textarea").first
        if not ta.is_visible():
            print("Opening Step 7 editor...")
            edit_btns = page.locator("button[aria-label='Edit this step']").all()
            edit_btns[7].scroll_into_view_if_needed()
            time.sleep(0.5)
            dismiss_timer(page)
            edit_btns[7].click(force=True)
            time.sleep(2.0)
            dismiss_timer(page)
            ta.wait_for(state="visible", timeout=5000)

        print("Step 7 is open.")

        # 2. Hover thumbnail to reveal Remove
        thumbs = page.locator("img[src*='storage.googleapis.com'], img[src*='blob']").all()
        for t in thumbs:
            if t.is_visible():
                t.hover()
                time.sleep(0.5)

        rem_btn = page.locator("button[aria-label='Remove']").first
        if rem_btn.is_visible():
            print("Clicking Remove button...")
            rem_btn.click(force=True)
            time.sleep(1.5)
            dismiss_timer(page)

        # 3. Setup file chooser
        fc_done = [False]

        def on_fc(fc):
            print("File chooser event received!")
            fc.set_files(IMAGE_PATH)
            fc_done[0] = True
            print("Set file:", IMAGE_PATH)

        page.on("filechooser", on_fc)

        upload_btn = page.locator("button[aria-label='Upload files'], button:has-text('+')").first
        print("Clicking Upload button...")
        upload_btn.click(force=True)
        time.sleep(4.0)
        dismiss_timer(page)
        print("File chooser done:", fc_done[0])

        # 4. Fill concise prompt
        print("Filling prompt...")
        ta.fill(PROMPT_TEXT)
        time.sleep(1.0)
        dismiss_timer(page)

        page.screenshot(path="handshake/scratch/step7_filled_ready.png")
        print("Saved step7_filled_ready.png")

        # 5. Click submit button
        cancel_btn = page.locator("button:has-text('Cancel')").first
        parent = cancel_btn.locator("xpath=..")
        submit_btn = parent.locator("button").last
        print("Clicking submit arrow button...")
        submit_btn.click(force=True)

        # Wait and observe what happens over 10 seconds
        for i in range(10):
            time.sleep(1.0)
            dismiss_timer(page)
            # check for dialogs
            dlgs = page.locator("div[role='dialog']").all()
            for d in dlgs:
                if d.is_visible():
                    txt = d.inner_text().strip()
                    if "Start timer" not in txt:
                        print(f"Dialog at t={i}: {txt[:100]}")
                        # click confirm/delete/continue
                        for b in d.locator("button:has-text('Confirm'), button:has-text('Proceed'), button:has-text('Delete'), button:has-text('Continue')").all():
                            if b.is_visible():
                                print("Clicking dialog button:", b.inner_text())
                                b.click(force=True)
                                break

        page.screenshot(path="handshake/scratch/step7_after_submit_10s.png")
        print("Saved step7_after_submit_10s.png")

        # Check top bar save button
        save_btn = page.locator("button:has-text('Save')").first
        if save_btn.is_visible() and not save_btn.is_disabled():
            print("Clicking top bar Save button...")
            save_btn.click(force=True)
            time.sleep(2.0)
            dismiss_timer(page)

        page.screenshot(path="handshake/scratch/step7_final_save.png")
        print("Saved step7_final_save.png")


if __name__ == "__main__":
    main()
