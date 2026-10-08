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

    # Check if feedback sidebar is open
    sidebar = page.locator("div[data-testid='task-side-panel']")
    if sidebar.count() == 0 or not sidebar.first.is_visible():
        print("Feedback sidebar is not visible, clicking toggle...")
        fb_btn = page.locator("button[aria-label='Feedback']")
        if fb_btn.count() > 0:
            fb_btn.first.click()
            page.wait_for_timeout(1500)

    # Re-check dismiss if it appeared
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    sidebar_info = page.evaluate("""() => {
        const panel = document.querySelector("div[data-testid='task-side-panel']");
        if (!panel) return { error: "No panel found" };

        const text = panel.innerText;
        const buttons = Array.from(panel.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            disabled: b.disabled,
            ariaDisabled: b.getAttribute('aria-disabled'),
            rect: {
                x: Math.round(b.getBoundingClientRect().x),
                y: Math.round(b.getBoundingClientRect().y),
                w: Math.round(b.getBoundingClientRect().width),
                h: Math.round(b.getBoundingClientRect().height)
            }
        }));

        const tabs = Array.from(panel.querySelectorAll('[role=\"tab\"], fieldset label, fieldset button')).map(t => ({
            text: t.innerText.trim()
        }));

        return {
            text,
            buttons,
            tabs
        };
    }""")

    print("=== SIDEBAR INFO ===")
    if "error" in sidebar_info:
        print("Error:", sidebar_info["error"])
    else:
        print("Sidebar text:\n", sidebar_info["text"])
        print("\nSidebar buttons:")
        for b in sidebar_info["buttons"]:
            print(b)

    page.screenshot(path="handshake/scratch/feedback_panel_open_state.png")
    print("Screenshot saved to handshake/scratch/feedback_panel_open_state.png")
