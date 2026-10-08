from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    print(f"Connected to: {page.url}")

    # Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=2000):
        st_btn.click()
        page.wait_for_timeout(1000)
        print("Dismissed Start timer modal")

    # Dismiss 'Got it' toast if present
    got_it = page.locator("button:has-text('Got it')").first
    if got_it.is_visible(timeout=1000):
        got_it.click()
        page.wait_for_timeout(500)

    # Scroll prompt into view
    prompt_el = page.locator("text='Consider a flow network'").first
    if prompt_el.is_visible():
        prompt_el.scroll_into_view_if_needed()
        page.wait_for_timeout(1000)
        page.screenshot(path="scratch/prompt_area.png")
        print("Scrolled to prompt and took screenshot: scratch/prompt_area.png")

    # Check all elements with pencil / edit near prompt
    edit_icons = page.locator("button:has(svg), svg.lucide-pencil, [aria-label*='edit' i]").all()
    print(f"Found {len(edit_icons)} edit icons on page.")
    for i, icon in enumerate(edit_icons):
        try:
            vis = icon.is_visible()
            box = icon.bounding_box()
            tag = icon.evaluate("el => el.tagName")
            cls = icon.get_attribute("class") or ""
            aria = icon.get_attribute("aria-label") or ""
            print(f"  Icon {i}: vis={vis} tag={tag} box={box} cls='{cls}' aria='{aria}'")
        except Exception as e:
            print(f"  Icon {i} err: {e}")
