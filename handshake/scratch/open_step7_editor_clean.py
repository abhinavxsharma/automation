import sys
import time

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Wait for hydration
    page.wait_for_selector("text=Computer Systems", timeout=15000)

    # Scroll directly to button 7
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print("Found edit buttons:", len(edit_btns))
    btn7 = edit_btns[7]
    btn7.scroll_into_view_if_needed()
    time.sleep(1)

    page.screenshot(path="handshake/scratch/btn7_in_view.png")
    print("Saved btn7_in_view.png")

    # Click button 7
    print("Clicking btn7...")
    btn7.click(force=True)
    time.sleep(2)

    page.screenshot(path="handshake/scratch/after_btn7_click.png")
    print("Saved after_btn7_click.png")

    # Check textarea
    ta = page.locator("textarea").first
    print("Textarea visible:", ta.is_visible())
    if ta.is_visible():
        print("Textarea value:\n", ta.input_value()[:120])

    # Check images / thumbnails inside editor
    imgs = page.locator("textarea ~ div img, [class*='rosetta'] img").all()
    print("Thumbnails found:", len(imgs))
    for i, im in enumerate(imgs):
        print(
            f"Thumbnail {i}: visible={im.is_visible()}, src={im.get_attribute('src')[:80]}"
        )

    rem_btns = page.locator("button[aria-label='Remove']").all()
    print("Remove buttons:", len(rem_btns))
    for i, r in enumerate(rem_btns):
        print(f"Remove button {i}: visible={r.is_visible()}")
