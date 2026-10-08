import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # 1. Dismiss timer modal if present
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        box = st.bounding_box()
        if box:
            print("Clicking Start timer at:", box)
            page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
            page.wait_for_timeout(1000)
            
    # 2. Scroll to step 14
    page.wait_for_selector("button[aria-label='Edit this step']", timeout=10000)
    btns = page.locator("button[aria-label='Edit this step']").all()
    print("Found btns:", len(btns))
    
    target_btn = btns[14]
    target_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    
    # Click it
    target_btn.click()
    print("Clicked Edit on Step 14!")
    page.wait_for_timeout(2000)
    
    page.screenshot(path="scratch/step14_opened_inspect.png")
    
    # Find all inputs, radios, or clickable elements in Step 14
    items = page.evaluate("""() => {
        // Find cancel button to locate the active editor
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button found" };
        const editorContainer = cancelBtn.closest('div.border, div.rounded-lg, form, section') || cancelBtn.parentElement.parentElement;
        
        const inputs = Array.from(editorContainer.querySelectorAll('input, [role=\"radio\"], label, button'));
        return {
            containerClass: editorContainer.className,
            elements: inputs.map(el => ({
                tag: el.tagName,
                type: el.type || '',
                role: el.getAttribute('role') || '',
                text: el.innerText ? el.innerText.slice(0, 60).replace(/\\n/g, ' ') : '',
                value: el.value || '',
                checked: el.checked || el.getAttribute('aria-checked')
            }))
        };
    }""")
    print("Editor container:", items.get("containerClass"))
    for el in items.get("elements", []):
        print("  ", el)
