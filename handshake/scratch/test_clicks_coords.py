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
                page.wait_for_timeout(500)

    # 1. Dismiss timer
    dismiss_timer()

    # 2. Check sidebar
    close_btn = page.locator("button[aria-label='Close']")
    if close_btn.count() == 0 or not close_btn.first.is_visible():
        page.evaluate("""() => {
            const btn = document.querySelector("button[aria-label='Feedback']");
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(1000)
    dismiss_timer()

    # 3. Inspect what happens when clicking Disagree
    print("Clicking Disagree icon at center (1056, 199)...")
    page.mouse.click(1056, 199)
    page.wait_for_timeout(1000)
    dismiss_timer()

    page.screenshot(path="handshake/scratch/after_click_disagree_icon.png")

    # 4. Inspect what happens when clicking Next at (946, 725)
    print("Clicking Next button at center (946, 725)...")
    page.mouse.click(946, 725)
    page.wait_for_timeout(1000)
    dismiss_timer()

    page.screenshot(path="handshake/scratch/after_click_next_coord.png")

    # 5. Read entire sidebar DOM text and buttons
    sidebar_after = page.evaluate("""() => {
        const panel = document.querySelector("div[data-testid='task-side-panel']");
        const btns = Array.from(panel ? panel.querySelectorAll('button') : []).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            classes: b.className.slice(0, 40),
            rect: b.getBoundingClientRect()
        }));
        return {
            text: panel ? panel.innerText : 'No panel',
            buttons: btns
        };
    }""")

    print("\n=== SIDEBAR STATE AFTER BOTH CLICKS ===")
    print("Text:\n", sidebar_after["text"])
    print("\nButtons:")
    for b in sidebar_after["buttons"]:
        print(b)
