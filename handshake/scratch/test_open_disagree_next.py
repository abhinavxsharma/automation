import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    def dismiss_timer():
        st_btn = page.locator("button:has-text('Start timer')")
        if st_btn.count() > 0 and st_btn.first.is_visible():
            box = st_btn.first.bounding_box()
            if box:
                print("Dismissing timer modal...")
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                page.wait_for_timeout(1000)

    # 1. Dismiss timer
    dismiss_timer()

    # 2. Check if sidebar is open by looking for Close button
    close_btn = page.locator("button[aria-label='Close']")
    if close_btn.count() == 0 or not close_btn.first.is_visible():
        print("Sidebar is closed, clicking Feedback button to open it...")
        fb_btn = page.locator("button[aria-label='Feedback']")
        if fb_btn.count() > 0:
            fb_btn.first.click()
            page.wait_for_timeout(1500)
    else:
        print("Sidebar is already open.")

    dismiss_timer()

    # 3. Check Disagree button
    disagree_btn = page.locator("button[aria-label='Disagree']")
    print("Found Disagree buttons:", disagree_btn.count())
    if disagree_btn.count() > 0 and disagree_btn.first.is_visible():
        print("Clicking Disagree button...")
        disagree_btn.first.click(force=True)
        page.wait_for_timeout(1500)

    dismiss_timer()

    # 4. Check if Next button is visible
    next_btn = page.locator("button:has-text('Next')")
    print("Found Next button:", next_btn.count())
    if next_btn.count() > 0 and next_btn.first.is_visible():
        print("Clicking Next button...")
        next_btn.first.click(force=True)
        page.wait_for_timeout(1500)

    dismiss_timer()

    # 5. Check what is now in the sidebar
    state = page.evaluate("""() => {
        const panel = document.querySelector("[data-testid='task-side-panel']") ||
                      Array.from(document.querySelectorAll('*')).find(el => el.getBoundingClientRect().x > 750 && el.getBoundingClientRect().width > 200 && el.getBoundingClientRect().height > 400);
        
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        
        return {
            panelText: panel ? panel.innerText : 'No panel found',
            submitBtn: submitBtn ? {
                text: submitBtn.innerText,
                disabled: submitBtn.disabled,
                ariaDisabled: submitBtn.getAttribute('aria-disabled')
            } : null
        };
    }""")

    print("\n=== CURRENT SIDEBAR STATE ===")
    print("Text:\n", state["panelText"])
    print("\nSubmit button:", state["submitBtn"])

    page.screenshot(path="handshake/scratch/after_disagree_and_next.png")
    print("Screenshot saved to handshake/scratch/after_disagree_and_next.png")
