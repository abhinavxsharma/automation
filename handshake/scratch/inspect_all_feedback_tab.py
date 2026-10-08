import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing timer modal...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # Click the "All" tab in Feedback panel
    all_tab = page.locator("button:has-text('All'), [role='tab']:has-text('All')")
    print("Found All tab:", all_tab.count())
    if all_tab.count() > 0:
        all_tab.first.click()
        page.wait_for_timeout(1000)

    # Inspect all items in Feedback panel under "All"
    panel_details = page.evaluate("""() => {
        // Find all cards or items in the right column
        const rightCol = Array.from(document.querySelectorAll('*')).filter(el => {
            const r = el.getBoundingClientRect();
            return r.x > 750 && r.width > 200 && r.height > 400;
        });

        // Let's get the text of the right panel
        const panel = document.querySelector("[data-testid='task-side-panel']") || rightCol[0];
        
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        
        return {
            panelText: panel ? panel.innerText : 'None',
            submitBtn: submitBtn ? {
                text: submitBtn.innerText,
                disabled: submitBtn.disabled,
                ariaDisabled: submitBtn.getAttribute('aria-disabled'),
                className: submitBtn.className,
                rect: submitBtn.getBoundingClientRect()
            } : null
        };
    }""")

    print("=== FEEDBACK ALL TAB TEXT ===")
    print(panel_details["panelText"])
    print("\n=== SUBMIT BUTTON ===")
    print(panel_details["submitBtn"])

    page.screenshot(path="handshake/scratch/feedback_all_tab_inspected.png")
    print("Screenshot saved to handshake/scratch/feedback_all_tab_inspected.png")
