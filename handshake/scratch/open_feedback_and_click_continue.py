import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser, page = get_task_page(p)

    for i in range(20):
        if page.locator("button").count() > 5:
            break
        page.wait_for_timeout(500)

    # 1. Dismiss timer modal if present
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        print("Dismissing timer modal...")
        modal_btn.first.click()
        page.wait_for_timeout(500)

    # 2. Click Continue on Science Judge card
    cont_btn = page.locator("button:has-text('Continue')").first
    if cont_btn.is_visible():
        print("Clicking Continue on Science Judge...")
        cont_btn.click()
        page.wait_for_timeout(2000)

    # 3. Check if Feedback sidebar is open; if not, open it
    fb_header = page.locator("text=Feedback")
    if fb_header.count() == 0 or not fb_header.first.is_visible():
        print("Feedback panel closed. Clicking toggle button in top bar...")
        # Find top right buttons
        top_btns = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('header button, nav button, button')).filter(b => {
                const r = b.getBoundingClientRect();
                return r.top < 60 && r.left > 800 && r.left < 900;
            }).map(b => ({ text: b.innerText, rect: b.getBoundingClientRect() }));
        }""")
        print("Top right buttons:", top_btns)
        if top_btns:
            target = top_btns[0]
            x = target['rect']['x'] + target['rect']['width'] / 2
            y = target['rect']['y'] + target['rect']['height'] / 2
            print(f"Clicking at ({x}, {y})...")
            page.mouse.click(x, y)
            page.wait_for_timeout(1000)

    page.screenshot(path="scratch/after_science_judge_continue.png")
    print("Saved scratch/after_science_judge_continue.png")

    body_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body_text.splitlines() if ln.strip()]
    print("\n--- Last 35 lines of page text ---")
    for ln in lines[-35:]:
        print(" ", ln)
