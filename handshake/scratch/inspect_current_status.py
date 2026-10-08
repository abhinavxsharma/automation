import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    panel = page.locator("div[data-testid='task-side-panel']")
    print("=== SIDE PANEL TEXT ===")
    if panel.count() > 0:
        print(panel.first.inner_text())
    else:
        print("Panel not found")

    print("\n=== BOTTOM BUTTONS IN SIDE PANEL ===")
    buttons = page.evaluate("""() => {
        const panel = document.querySelector("div[data-testid='task-side-panel']");
        if (!panel) return [];
        return Array.from(panel.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            disabled: b.disabled,
            ariaDisabled: b.getAttribute('aria-disabled'),
            classes: b.className
        }));
    }""")
    for b in buttons:
        print(b)
