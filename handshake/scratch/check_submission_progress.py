import json
import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    def dismiss_timer():
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible():
            b = st.bounding_box()
            if b:
                page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                page.wait_for_timeout(1000)

    dismiss_timer()
    print("Waiting 5 seconds for network request / modal...")
    page.wait_for_timeout(5000)
    dismiss_timer()

    # Check for confirmation modal (e.g. 'Confirm time')
    confirm_info = page.evaluate("""() => {
        const dialog = document.querySelector('div[role=\"dialog\"], [role=\"alertdialog\"], div[class*=\"z-50\"]');
        const btns = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            classes: b.className,
            rect: b.getBoundingClientRect()
        })).filter(b => b.text || b.aria);

        return {
            url: window.location.href,
            title: document.title,
            hasDialog: !!dialog,
            dialogText: dialog ? dialog.innerText : null,
            buttons: btns,
            bodySnippet: document.body.innerText.slice(0, 300)
        };
    }""")
    print("\nPost-submit state:\n", json.dumps(confirm_info, indent=2))

    # Click Confirm time if visible
    confirm_btn = page.locator("button:has-text('Confirm time'), button:has-text('Confirm'), button:has-text('Submit anyway'), button:has-text('Yes')").first
    if confirm_btn.count() > 0 and confirm_btn.is_visible():
        btn_txt = confirm_btn.inner_text().strip()
        print(f"\n>>> Found confirmation button: '{btn_txt}'. Clicking... <<<")
        confirm_btn.click()
        page.wait_for_timeout(5000)

    dismiss_timer()

    page.screenshot(path="handshake/scratch/submission_confirmation_check.png")
    print("Screenshot saved to handshake/scratch/submission_confirmation_check.png")
    print("Current URL:", page.url)
    print("Current Title:", page.title())
