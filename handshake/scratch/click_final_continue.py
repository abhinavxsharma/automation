import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # 1. Dismiss timer modal
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        print("Dismissing timer modal...")
        modal_btn.first.click()
        page.wait_for_timeout(500)

    # 2. Click Continue on "You're done, congrats!"
    cont_btn = page.locator("button:has-text('Continue')").first
    print("Continue button visible:", cont_btn.is_visible(), "enabled:", cont_btn.is_enabled())
    if cont_btn.is_visible() and cont_btn.is_enabled():
        print("Clicking Continue...")
        cont_btn.click()
        page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_final_continue.png")
    print("Saved scratch/after_final_continue.png")

    body_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body_text.splitlines() if ln.strip()]
    print("\n--- Last 35 lines of page text ---")
    for ln in lines[-35:]:
        print(" ", ln)

    # Find any Submit buttons on page
    submit_btns = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button')).filter(b => 
            b.innerText.toLowerCase().includes('submit') || b.innerText.toLowerCase().includes('finish')
        ).map(b => ({
            text: b.innerText,
            visible: b.offsetParent !== null,
            enabled: !b.disabled,
            rect: b.getBoundingClientRect()
        }));
    }""")
    print("\nSubmit buttons found:", submit_btns)
