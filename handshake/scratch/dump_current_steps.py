import sys
from pathlib import Path
sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        st_btn.first.click()
        page.wait_for_timeout(1000)

    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print(f"Total edit buttons found: {len(edit_btns)}")

    steps_info = []
    for idx, btn in enumerate(edit_btns):
        # get enclosing card text
        card_text = btn.evaluate("""el => {
            let p = el.parentElement;
            while (p && !p.getAttribute('data-block-id') && !p.className.includes('rounded') && p !== document.body) {
                p = p.parentElement;
            }
            return p ? p.innerText : '';
        }""")
        steps_info.append(f"=== STEP {idx} ===\n{card_text}\n")

    with open("handshake/scratch/current_all_steps.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(steps_info))

    print("Saved all steps to handshake/scratch/current_all_steps.txt")
