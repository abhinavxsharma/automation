import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(2000)
    
    # 1. Dismiss timer modal
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        box = st.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            print("Dismissed timer modal")
            page.wait_for_timeout(1000)
            
    # 2. Find Error Type 'Edit this step' button
    # In find_all_edits_1520.py, button index 14 was:
    # [14] box={'x': 750.5, 'y': 7988.0} near: Error Type Select the error type that best describes...
    btns = page.locator("button[aria-label='Edit this step']").all()
    print("Total edit buttons:", len(btns))
    
    # Let's find the one near 'Connectivity / topology error'
    target_btn = None
    for i, btn in enumerate(btns):
        txt = btn.evaluate("el => el.closest('div.flex-col, div[data-block-id], section')?.innerText || ''")
        if 'error type' in txt.lower():
            print(f"Found Error Type edit button at index {i}!")
            target_btn = btn
            break
            
    if target_btn:
        target_btn.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        target_btn.click()
        print("Clicked Error Type edit button!")
        page.wait_for_timeout(2000)
    else:
        print("Target button not found by text, trying index 14...")
        if len(btns) > 14:
            btns[14].scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            btns[14].click()
            page.wait_for_timeout(2000)
            
    page.screenshot(path="scratch/error_type_opened.png")
    
    # Check what interactive elements appeared in this container
    elements = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('input, select, textarea, button, [role=\"radio\"], [role=\"combobox\"], [role=\"option\"]'));
        return els.map(e => ({
            tag: e.tagName,
            type: e.type || '',
            role: e.getAttribute('role') || '',
            aria: e.getAttribute('aria-label') || '',
            text: e.innerText ? e.innerText.trim().slice(0, 50) : '',
            value: e.value || ''
        })).filter(x => x.text || x.aria || x.value);
    }""")
    print("Interactive elements count:", len(elements))
    for el in elements:
        if any(w in el['text'].lower() or w in el['value'].lower() for w in ['label', 'connectivity', 'cancel', 'save', 'mis-binding']):
            print("  MATCH:", el)
