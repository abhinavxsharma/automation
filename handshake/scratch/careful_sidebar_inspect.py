import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # 1. Dismiss timer modal if visible
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing timer modal...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # Check if sidebar open
    def is_sidebar_open():
        return page.evaluate("""() => {
            const closeBtn = document.querySelector("button[aria-label='Close']");
            if (closeBtn && closeBtn.getBoundingClientRect().width > 0) return true;
            const panel = document.querySelector("[data-testid='task-side-panel']");
            if (panel && panel.getBoundingClientRect().width > 0) return true;
            return false;
        }""")

    print("Initial is_sidebar_open:", is_sidebar_open())
    if not is_sidebar_open():
        print("Opening sidebar...")
        page.locator("button[aria-label='Feedback']").first.click()
        page.wait_for_timeout(1500)
        print("After click is_sidebar_open:", is_sidebar_open())

    # Dismiss timer modal again if needed
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # Inspect all elements in sidebar
    sidebar_data = page.evaluate("""() => {
        const panel = document.querySelector("[data-testid='task-side-panel']");
        if (!panel) return { error: "No panel found" };

        const allButtons = Array.from(panel.querySelectorAll('button')).map(b => ({
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

        return {
            text: panel.innerText,
            buttons: allButtons
        };
    }""")

    print("Sidebar data:")
    print("Text:\n", sidebar_data.get("text"))
    print("\nButtons:")
    for b in sidebar_data.get("buttons", []):
        print(b)

    page.screenshot(path="handshake/scratch/sidebar_careful_inspect.png")
