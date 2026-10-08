import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # 1. Dismiss timer modal
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing timer modal...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Click aria-label="Disagree"
    disagree_btn = page.locator("button[aria-label='Disagree']")
    print("Found Disagree button:", disagree_btn.count())
    if disagree_btn.count() > 0:
        print("Clicking Disagree button...")
        disagree_btn.first.click(force=True)
        page.wait_for_timeout(1500)

    # Dismiss modal if it appeared again
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 3. Check what happened to sidebar
    after_info = page.evaluate("""() => {
        const rightEls = Array.from(document.querySelectorAll('*')).filter(el => {
            const r = el.getBoundingClientRect();
            return r.x > 700 && r.width > 200 && r.height > 500;
        });
        const btns = Array.from(document.querySelectorAll('button')).filter(b => b.getBoundingClientRect().x > 700);
        return {
            text: rightEls[0] ? rightEls[0].innerText : "None",
            buttons: btns.map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                disabled: b.disabled,
                ariaDisabled: b.getAttribute('aria-disabled')
            }))
        };
    }""")
    print("=== AFTER DISAGREE CLICK ===")
    print("Text:\n", after_info["text"])
    print("\nButtons:")
    for b in after_info["buttons"]:
        print(b)

    page.screenshot(path="handshake/scratch/after_clean_disagree.png")
    print("Screenshot saved to handshake/scratch/after_clean_disagree.png")
