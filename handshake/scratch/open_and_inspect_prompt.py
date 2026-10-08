import time

from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    for _ in range(20):
        if "Final Answer" in page.evaluate("() => document.body ? document.body.innerText : ''"):
            break
        time.sleep(0.5)

    def dismiss():
        st_btn = page.locator("button:has-text('Start timer')").first
        if st_btn.is_visible(timeout=1000):
            st_btn.click()
            page.wait_for_timeout(1000)

    dismiss()

    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print(f"Total edit buttons: {len(edit_btns)}")
    if len(edit_btns) > 7:
        print("Clicking edit_btns[7]...")
        edit_btns[7].scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        edit_btns[7].click(force=True)
        page.wait_for_timeout(1500)
        dismiss()

    page.screenshot(path="scratch/prompt_editor_open.png")
    print("Screenshot saved to scratch/prompt_editor_open.png")

    # Inspect all elements inside the prompt editor card
    editor_info = page.evaluate("""() => {
        const ta = document.querySelector('textarea');
        const fileInp = document.querySelector('input[type="file"]');
        const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText,
            aria: b.getAttribute('aria-label'),
            className: b.className,
            box: b.getBoundingClientRect()
        }));
        return {
            hasTextarea: !!ta,
            textareaVal: ta ? ta.value.slice(0, 100) : null,
            hasFileInput: !!fileInp,
            buttons: buttons.filter(b => b.box.width > 0 && b.box.height > 0)
        };
    }""")
    print("Editor info:")
    print("  hasTextarea:", editor_info['hasTextarea'])
    print("  textareaVal:", editor_info['textareaVal'])
    print("  hasFileInput:", editor_info['hasFileInput'])
    print("  Visible buttons:")
    for b in editor_info['buttons']:
        print(f"    text='{b['text']}' aria='{b['aria']}' box=({b['box']['x']}, {b['box']['y']})")
