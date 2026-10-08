import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(2000)

    # Let's inspect all items in the feedback sidebar
    sidebar_items = page.evaluate("""() => {
        const sidePanel = document.querySelector('[data-testid="task-side-panel"]');
        if (!sidePanel) return { error: "No task-side-panel" };

        const items = Array.from(sidePanel.querySelectorAll('[role="button"], button')).map(el => ({
            tag: el.tagName,
            role: el.getAttribute('role'),
            text: el.innerText.trim(),
            aria: el.getAttribute('aria-label'),
            className: el.className
        }));

        // Find the Start button
        const startBtn = Array.from(sidePanel.querySelectorAll('button')).find(b => b.innerText.trim() === 'Start');

        return {
            itemsCount: items.length,
            items,
            startBtnDisabled: startBtn ? startBtn.disabled : null,
            startBtnVisible: startBtn ? startBtn.offsetParent !== null : null
        };
    }""")

    print(f"Sidebar items count: {sidebar_items.get('itemsCount')}")
    print(f"Start button disabled: {sidebar_items.get('startBtnDisabled')}")
    print("\nSidebar elements:")
    for it in sidebar_items.get("items", []):
        print(f"  [{it['tag']}|{it['role']}|aria={it['aria']}]: {it['text'][:60]}")
