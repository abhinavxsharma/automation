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
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    info = page.evaluate("""() => {
        const sidePanel = document.querySelector("[data-testid='task-side-panel']");
        const allTestIds = Array.from(document.querySelectorAll('[data-testid]')).map(el => el.getAttribute('data-testid'));
        const allButtons = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            x: Math.round(b.getBoundingClientRect().x),
            y: Math.round(b.getBoundingClientRect().y),
            w: Math.round(b.getBoundingClientRect().width),
            h: Math.round(b.getBoundingClientRect().height)
        }));
        
        return {
            hasSidePanel: !!sidePanel,
            sidePanelText: sidePanel ? sidePanel.innerText : null,
            allTestIds: allTestIds,
            allButtons: allButtons
        };
    }""")

    print("Has side panel:", info["hasSidePanel"])
    if info["hasSidePanel"]:
        print("Side panel text:\n", info["sidePanelText"])
    print("\nButtons:")
    for b in info["allButtons"]:
        if b["x"] > 600 or "save" in b["text"].lower() or "submit" in b["text"].lower() or "next" in b["text"].lower():
            print(b)
    
    page.screenshot(path="handshake/scratch/live_page_state.png")
    print("Screenshot saved to handshake/scratch/live_page_state.png")
