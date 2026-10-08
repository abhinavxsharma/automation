import sys

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_selector("text=Computer Systems", timeout=10000)

    # Click Button 7
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print("Clicking edit_btns[7]...")
    edit_btns[7].scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    edit_btns[7].click(force=True)
    page.wait_for_timeout(1500)

    # Screenshot
    page.screenshot(path="handshake/scratch/after_click_edit_btn7.png")
    print("Saved after_click_edit_btn7.png")

    # Inspect open dialogs or textareas
    dialogs = page.locator(
        "div[role='dialog'], div[role='alertdialog'], div[class*='modal']"
    ).all()
    print(f"Dialogs found: {len(dialogs)}")
    for d in dialogs:
        print("Dialog text:", d.inner_text()[:200])

    ta = page.locator("textarea").all()
    print(f"Textareas found: {len(ta)}")
    for t in ta:
        print("Textarea visible:", t.is_visible(), "val:", t.input_value()[:80])

    rem = page.locator("button[aria-label='Remove']").all()
    print(f"Remove buttons: {len(rem)}")
    for r in rem:
        print("Remove button visible:", r.is_visible())

    upload = page.locator(
        "button[aria-label='Upload files'], button:has-text('+'), input[type='file']"
    ).all()
    print(f"Upload elements: {len(upload)}")
    for u in upload:
        print("Upload element:", u.evaluate("(el) => el.outerHTML.slice(0, 100)"))
