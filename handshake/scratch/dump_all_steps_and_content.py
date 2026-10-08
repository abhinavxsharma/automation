import json
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Let's inspect the main steps
    # Usually in Handshake UI, steps are in a container or have headings or step numbers
    steps = page.locator("div[class*='step'], div[data-step], [class*='Step']").all()
    print(f"Found {len(steps)} candidate step containers.")

    # Let's look for all 'Edit this step' buttons
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print(f"Found {len(edit_btns)} 'Edit this step' buttons.")
    
    for i, btn in enumerate(edit_btns):
        try:
            # Find the parent card/section containing this edit button
            parent_text = btn.evaluate("""
                el => {
                    let cur = el.parentElement;
                    while (cur && !cur.innerText.includes('Step') && cur !== document.body) {
                        cur = cur.parentElement;
                    }
                    return cur ? cur.innerText.substring(0, 300) : 'NO PARENT FOUND';
                }
            """)
            print(f"\n--- Edit Button {i} ---")
            print(parent_text.replace('\n', ' -- '))
        except Exception as e:
            print(f"Error for btn {i}: {e}")

    # Also dump feedback / review sidebar
    feedback_items = page.locator("[class*='feedback'], [class*='Feedback'], [class*='comment']").all()
    print(f"\nFound {len(feedback_items)} feedback elements.")
    sidebar = page.locator("aside, [role='complementary'], div[class*='sidebar'], div[class*='drawer']").all()
    print(f"Found {len(sidebar)} sidebar elements.")
    for i, sb in enumerate(sidebar):
        if sb.is_visible():
            txt = sb.inner_text().strip()
            if txt:
                print(f"\n--- Visible Sidebar {i} ---")
                print(txt[:1000])
