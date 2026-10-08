import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DISTRACTORS = ["75", "73", "72", "68", "64"]

with sync_playwright() as p:
    browser, page = get_task_page(p)

    for i in range(20):
        if page.locator("button").count() > 5:
            break
        page.wait_for_timeout(500)

    # Helper to dismiss timer
    def dismiss_timer():
        modal_btn = page.locator("button:has-text('Start timer')")
        if modal_btn.count() > 0 and modal_btn.first.is_visible():
            print("Dismissing timer modal...")
            modal_btn.first.click()
            page.wait_for_timeout(500)

    dismiss_timer()

    # Click Continue on distractor guideline card
    cont = page.locator("button:has-text('Continue')").first
    if cont.is_visible() and cont.is_enabled():
        print("Clicking Continue on Distractor guideline...")
        cont.click()
        page.wait_for_timeout(1500)

    dismiss_timer()

    # Fill distractors one by one
    for idx, d_val in enumerate(DISTRACTORS):
        print(f"\n--- Processing Distractor {idx + 1}: {d_val} ---")
        dismiss_timer()
        
        # Wait for input
        inp = None
        for _ in range(10):
            inp = page.locator("textarea, input[placeholder*='typing'], input[type='text'], [contenteditable='true']").first
            if inp.count() > 0 and inp.is_visible():
                break
            page.wait_for_timeout(500)
            dismiss_timer()

        if inp and inp.is_visible():
            print(f"Filling Distractor {idx + 1} with '{d_val}'...")
            inp.fill(d_val)
            page.wait_for_timeout(500)
            page.evaluate(f"""() => {{
                const el = document.querySelector("textarea, input[placeholder*='typing'], input[type='text'], [contenteditable='true']");
                if (el) {{
                    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
                        el.value = {d_val!r};
                        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }} else {{
                        el.innerText = {d_val!r};
                        el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                }}
            }}""")
            page.wait_for_timeout(500)

            # Click Continue
            c_btn = page.locator("button:has-text('Continue')").first
            if c_btn.is_visible() and c_btn.is_enabled():
                print(f"Clicking Continue for Distractor {idx + 1}...")
                c_btn.click()
                page.wait_for_timeout(2000)
        else:
            print(f"No input found for Distractor {idx + 1}!")
            break

    dismiss_timer()
    page.screenshot(path="scratch/after_all_distractors.png")
    print("Saved scratch/after_all_distractors.png")

    body_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body_text.splitlines() if ln.strip()]
    print("\n--- Last 35 lines of page text ---")
    for ln in lines[-35:]:
        print(" ", ln)
