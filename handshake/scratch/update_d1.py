import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(2000)

    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        st_btn.first.click()
        page.wait_for_timeout(1000)

    # Cancel any open editor
    cancel_btn = page.locator("button:has-text('Cancel')")
    if cancel_btn.count() > 0 and cancel_btn.first.is_visible():
        cancel_btn.first.click()
        page.wait_for_timeout(1000)

    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    print(f"Total edit_btns: {len(edit_btns)}")

    # Distractor 1 is edit_btns[18]
    d1_btn = edit_btns[18]
    d1_card_text = d1_btn.evaluate("el => el.closest('div.border, section, [data-block-id]').innerText")
    print("D1 before:\n", d1_card_text)

    # Click edit on D1
    d1_btn.click()
    page.wait_for_timeout(1000)

    # Find the textarea
    ta = page.locator("textarea[placeholder='Plausible-but-wrong answer text']").first
    if not ta.is_visible():
        ta = page.locator("textarea").first
    print("Current textarea value:", repr(ta.input_value()))

    # Fill target value: $(A+\overline{B})C$
    target_val = r"$(A+\overline{B})C$"
    ta.fill(target_val)
    page.wait_for_timeout(500)
    print("New textarea value:", repr(ta.input_value()))

    # Click the commit button (the up arrow inside the editor card)
    commit_btn = page.locator("button:has(svg.lucide-arrow-up), button:has(svg.lucide-send)").first
    print("Commit button visible:", commit_btn.is_visible())
    commit_btn.click()
    page.wait_for_timeout(1500)

    # Verify D1 rendered text
    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    d1_card_after = edit_btns[18].evaluate("el => el.closest('div.border, section, [data-block-id]').innerHTML")
    print("D1 HTML after:\n", d1_card_after[:400])

    page.screenshot(path="handshake/scratch/after_d1_updated.png")
    print("Screenshot saved to handshake/scratch/after_d1_updated.png")
