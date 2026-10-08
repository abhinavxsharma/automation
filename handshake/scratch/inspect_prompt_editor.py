from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(1000)

    # Let's inspect the textarea
    ta = page.locator("textarea").first
    print("Textarea visible:", ta.is_visible())
    if ta.is_visible():
        print("Current textarea text:\n", ta.input_value()[:200])

    # Let's find file inputs
    file_inputs = page.locator("input[type='file']").all()
    print(f"File inputs found: {len(file_inputs)}")
    for fi in file_inputs:
        print("  File input:", fi.get_attribute("accept"), fi.is_visible())

    # Let's find remove / delete image buttons
    remove_btns = page.locator("button[aria-label*='delete' i], button[aria-label*='remove' i], button:has(svg.lucide-x), button:has(svg.lucide-trash)").all()
    print(f"Remove buttons found: {len(remove_btns)}")
    for rb in remove_btns:
        print("  Remove btn:", rb.get_attribute("aria-label"), rb.bounding_box())

    # Let's find the submit / up-arrow button
    submit_btn = page.locator("button:has(svg.lucide-arrow-up), button:has(svg.lucide-send), button[type='submit']").all()
    print(f"Submit buttons found: {len(submit_btn)}")
    for sb in submit_btn:
        print("  Submit btn:", sb.get_attribute("aria-label"), sb.bounding_box())

    page.screenshot(path="scratch/prompt_editor_inspect.png")
    print("Saved scratch/prompt_editor_inspect.png")
