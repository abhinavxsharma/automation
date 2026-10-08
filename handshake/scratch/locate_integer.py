import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    int_els = page.locator("text='Integer'").all()
    print("Found Integer elements:", len(int_els))
    for i, el in enumerate(int_els):
        box = el.bounding_box()
        tag = el.evaluate("e => e.tagName")
        parent_tag = el.evaluate("e => e.parentElement.tagName")
        parent_cls = el.evaluate("e => e.parentElement.className")
        print(f"  Element {i}: vis={el.is_visible()} box={box} tag={tag} parent={parent_tag}.{parent_cls[:30]}")

    if int_els:
        print("Clicking first Integer element...")
        int_els[0].click(force=True)
        page.wait_for_timeout(1000)

        # Check if circle is filled
        page.screenshot(path="scratch/after_direct_int_click.png")
        print("Saved scratch/after_direct_int_click.png")

        # Now click Continue
        cont_btn = page.locator("button:has-text('Continue')").first
        if cont_btn.is_visible():
            print("Clicking Continue...")
            cont_btn.click(force=True)
            page.wait_for_timeout(2000)
            page.screenshot(path="scratch/after_int_continue_clean.png")
            print("Saved scratch/after_int_continue_clean.png")
