import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button[aria-label='Edit this step']", timeout=10000)
    
    # 1. Dismiss timer modal if present
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        st.click()
        page.wait_for_timeout(1000)
        
    # 2. Find the container with 'Error Type'
    error_type_header = page.locator("text='Error Type'").first
    error_type_header.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    
    # Find the edit button near Error Type
    # In the UI, the edit button (pencil) is in the same block
    container = error_type_header.locator("xpath=ancestor::div[contains(@class, 'flex') and contains(@class, 'gap')][last()]")
    edit_btn = container.locator("button[aria-label='Edit this step']").first
    if not edit_btn.is_visible():
        # Fallback to finding by proximity
        all_edits = page.locator("button[aria-label='Edit this step']").all()
        for eb in all_edits:
            txt = eb.evaluate("el => (el.closest('div.flex-col, div[data-block-id], section') || el.parentElement)?.innerText || ''")
            if "error type" in txt.lower():
                edit_btn = eb
                break
                
    print("Found edit_btn visible:", edit_btn.is_visible())
    edit_btn.click()
    print("Clicked Edit Step 14!")
    page.wait_for_timeout(1500)
    
    page.screenshot(path="scratch/step14_active_editor.png")
    
    # Check what appears
    cancel = page.locator("button:has-text('Cancel')").first
    print("Cancel button visible:", cancel.is_visible())
