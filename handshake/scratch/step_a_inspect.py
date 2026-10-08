import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Wait for page to be ready
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # 1. Dismiss timer if visible
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing Start timer...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Check all buttons in the top navbar (y < 60)
    btns = page.locator("button").all()
    print("Top navbar buttons:")
    for b in btns:
        box = b.bounding_box()
        if box and box["y"] < 50:
            txt = b.inner_text().strip()
            aria = b.get_attribute("aria-label") or ""
            print(f"  text='{txt}' aria='{aria}' box={box}")

    # If feedback sidebar is not open, click the button at (926, 23)
    sidebar_visible = page.evaluate("""() => {
        const h = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.trim() === 'Feedback' && e.getBoundingClientRect().width > 0);
        return !!h;
    }""")
    print("Sidebar visible before click:", sidebar_visible)
    if not sidebar_visible:
        print("Clicking feedback icon at (926, 23)...")
        page.mouse.click(926, 23)
        page.wait_for_timeout(1000)

    # Check sidebar again
    sidebar_text = page.evaluate("""() => {
        const cards = Array.from(document.querySelectorAll('*')).filter(e => e.innerText && (e.innerText.includes('items addressed') || e.innerText.includes('Science Judge')));
        return cards.map(c => c.innerText).slice(0, 5);
    }""")
    print("Sidebar text snippets:", len(sidebar_text))

    page.screenshot(path="scratch/step_a_inspect.png")
    print("Saved step_a_inspect.png")
