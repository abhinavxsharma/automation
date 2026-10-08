import time

from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Wait for content
    for _ in range(20):
        if "Final Answer" in page.evaluate("() => document.body ? document.body.innerText : ''"):
            break
        time.sleep(0.5)

    # Dismiss timer modal
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(1000)

    # Scroll Btn 17 into view
    # Btn 17 is the Edit button near diagram_25449.png
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print(f"Found {len(edit_btns)} 'Edit this step' buttons")

    # Let's inspect each edit button and its surrounding text
    for i, eb in enumerate(edit_btns):
        parent_text = eb.evaluate("el => el.closest('div[class*=\"group\"], div[class*=\"card\"], div[class*=\"item\"], div')?.innerText?.slice(0, 100) || ''")
        box = eb.bounding_box()
        print(f"Edit button {i}: box={box} near: {parent_text!r}")

    # Let's target the edit button near prompt or image
    prompt_edit_btn = None
    for eb in edit_btns:
        parent_text = eb.evaluate("el => el.closest('div')?.parentElement?.innerText || ''")
        if "Consider a flow network" in parent_text or "diagram" in parent_text or "Enter your prompt" in parent_text:
            prompt_edit_btn = eb
            break

    if prompt_edit_btn:
        print("Found prompt edit button! Clicking it...")
        prompt_edit_btn.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        prompt_edit_btn.click(force=True)
        page.wait_for_timeout(2000)
        page.screenshot(path="scratch/after_prompt_edit_click.png")
        print("Saved scratch/after_prompt_edit_click.png")
    else:
        print("Prompt edit button not identified by text.")
