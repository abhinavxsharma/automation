import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # 1. Dismiss timer
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        b = st.bounding_box()
        if b:
            page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Click feedback toggle via DOM click
    print("Clicking Feedback toggle via DOM...")
    page.evaluate("""() => {
        const btn = document.querySelector("button[aria-label='Feedback']");
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1500)

    # Dismiss timer if it appeared
    if st.is_visible():
        b = st.bounding_box()
        if b:
            page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
            page.wait_for_timeout(1000)

    # 3. Dump all elements in right 350px of the viewport
    right_elements = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*')).filter(el => {
            const r = el.getBoundingClientRect();
            return r.x > 750 && r.width > 0 && r.height > 0;
        });

        return all.map(el => ({
            tag: el.tagName,
            role: el.getAttribute('role'),
            text: el.innerText ? el.innerText.trim().slice(0, 50) : '',
            aria: el.getAttribute('aria-label'),
            type: el.getAttribute('type'),
            disabled: el.disabled,
            ariaDisabled: el.getAttribute('aria-disabled'),
            rect: {
                x: Math.round(el.getBoundingClientRect().x),
                y: Math.round(el.getBoundingClientRect().y),
                w: Math.round(el.getBoundingClientRect().width),
                h: Math.round(el.getBoundingClientRect().height)
            }
        })).filter(el => el.tag === 'BUTTON' || el.role === 'button' || el.aria || el.type === 'radio' || el.text.includes('Submit') || el.text.includes('Next') || el.text.includes('addressed') || el.text.includes('attention'));
    }""")

    print(f"Found {len(right_elements)} interactive elements on right:")
    for el in right_elements:
        print(el)

    page.screenshot(path="handshake/scratch/sidebar_dom_clicked.png")
    print("Saved handshake/scratch/sidebar_dom_clicked.png")
