import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # 1. Dismiss timer
    def dismiss_timer():
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible():
            b = st.bounding_box()
            if b:
                page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                page.wait_for_timeout(1000)

    dismiss_timer()

    # 2. Ensure sidebar is open
    is_open = page.evaluate("""() => {
        const closeBtn = document.querySelector("button[aria-label='Close']");
        return !!(closeBtn && closeBtn.getBoundingClientRect().width > 0);
    }""")
    if not is_open:
        print("Sidebar closed, clicking Feedback toggle...")
        page.mouse.click(938, 23)
        page.wait_for_timeout(1500)
    dismiss_timer()

    # 3. Check current tab and items
    panel_info = page.evaluate("""() => {
        const rightContainer = Array.from(document.querySelectorAll('*')).find(el => {
            const r = el.getBoundingClientRect();
            return r.x > 740 && r.width > 200 && r.height > 500;
        });

        const allButtons = Array.from(document.querySelectorAll('button')).map(b => {
            const r = b.getBoundingClientRect();
            return {
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                disabled: b.disabled,
                ariaDisabled: b.getAttribute('aria-disabled'),
                classes: b.className,
                rect: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }
            };
        }).filter(b => b.rect.x > 740);

        return {
            text: rightContainer ? rightContainer.innerText : 'None',
            buttons: allButtons
        };
    }""")

    print("=== CURRENT PANEL ===")
    print("Text:\n", panel_info["text"])
    print("\nButtons on right:")
    for b in panel_info["buttons"]:
        print(b)

    page.screenshot(path="handshake/scratch/deep_inspect_start.png")
