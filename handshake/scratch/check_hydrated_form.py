import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser, page = get_task_page(p)
    print("Connected to task page:", page.url)

    # Wait for page to fully hydrate
    for i in range(20):
        btn_count = page.locator("button").count()
        if btn_count > 5:
            print(f"Hydrated! Found {btn_count} buttons after {i*0.5}s")
            break
        page.wait_for_timeout(500)

    # Dismiss timer modal if present
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        print("Dismissing timer modal...")
        page.mouse.click(524, 443)
        page.wait_for_timeout(500)

    # Inspect all visible text and cards
    page.screenshot(path="scratch/hydrated_inspect.png")
    print("Saved scratch/hydrated_inspect.png")

    body_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body_text.splitlines() if ln.strip()]
    print("\n--- Last 30 lines of page text ---")
    for ln in lines[-30:]:
        print(" ", ln)

    # Find all inputs and textareas
    inputs = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('textarea, input, [contenteditable="true"]')).map(el => ({
            tag: el.tagName,
            placeholder: el.placeholder || '',
            value: (el.value || el.innerText || '').slice(0, 100),
            visible: el.offsetParent !== null,
            rect: el.getBoundingClientRect()
        }));
    }""")
    print("\nInputs found:", inputs)
