import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    print("Waiting for page load...")
    try:
        page.wait_for_selector("button:has-text('Save')", timeout=10000)
    except Exception as e:
        print("Wait timed out:", e)

    page.wait_for_timeout(2000)
    print("Body text length:", len(page.inner_text("body")))
    print("Body text preview:", page.inner_text("body")[:300])

    # Check for modals
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        print("Start timer visible, clicking...")
        st_btn.first.click()
        page.wait_for_timeout(1000)

    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print("Total Edit this step buttons:", len(edit_btns))

    cards = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        return btns.map((b, idx) => {
            let p = b.parentElement;
            while (p && !p.getAttribute('data-block-id') && p !== document.body) {
                p = p.parentElement;
            }
            return {
                idx,
                blockId: p ? p.getAttribute('data-block-id') : null,
                text: (p ? p.innerText : b.innerText).slice(0, 150).replace(/\\n+/g, ' ')
            };
        });
    }""")
    for c in cards:
        print(f"[{c['idx']}] id={c['blockId']}: {c['text']}")
