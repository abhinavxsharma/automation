import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # 1. Dismiss timer modal
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        st.click()
        print("Dismissed timer modal via click")
        page.wait_for_timeout(1000)
    else:
        # Check via JS if there's any Start timer button
        page.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(1000)
        
    # 2. Check if Cancel button is visible (meaning editor is open)
    cancel = page.locator("button:has-text('Cancel')").first
    print("Is editor open (Cancel visible):", cancel.is_visible())
    
    if not cancel.is_visible():
        # Open editor for step 14
        error_type_header = page.locator("text='Error Type'").first
        error_type_header.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        
        container = error_type_header.locator("xpath=ancestor::div[contains(@class, 'flex') and contains(@class, 'gap')][last()]")
        edit_btn = container.locator("button[aria-label='Edit this step']").first
        edit_btn.click()
        print("Re-opened editor for Step 14")
        page.wait_for_timeout(1000)
        
    # 3. Select 'Label–element or axis mis-binding' option
    # Find the element with text starting with Label
    sel_res = page.evaluate("""() => {
        // Find all elements that contain the label mis-binding text
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        let targetTextNode = null;
        while (node = walker.nextNode()) {
            if (node.nodeValue && node.nodeValue.includes('Label') && node.nodeValue.includes('mis-binding') && node.nodeValue.includes('reads every label correctly')) {
                targetTextNode = node;
                break;
            }
        }
        if (!targetTextNode) return { error: "Text node not found" };
        
        let el = targetTextNode.parentElement;
        // Find clickable row/item
        const clickable = el.closest('li, label, div[role=\"radio\"], div[role=\"button\"], div.cursor-pointer') || el;
        clickable.scrollIntoView({ behavior: 'instant', block: 'center' });
        clickable.click();
        return { success: true, tag: clickable.tagName, text: clickable.innerText.slice(0, 60) };
    }""")
    print("Select option result:", sel_res)
    page.wait_for_timeout(1000)
    
    # 4. Click the up-arrow commit button (next to Cancel)
    commit_res = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button" };
        const parent = cancelBtn.parentElement;
        const arrowBtn = Array.from(parent.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (arrowBtn) {
            arrowBtn.scrollIntoView({ behavior: 'instant', block: 'center' });
            arrowBtn.click();
            return { success: true };
        }
        return { error: "No arrow button next to Cancel" };
    }""")
    print("Commit result:", commit_res)
    page.wait_for_timeout(2000)
    
    page.screenshot(path="scratch/step14_committed_verified.png")
    
    # 5. Check what is now saved in Step 14
    page.wait_for_selector("button[aria-label='Edit this step']", timeout=10000)
    btns = page.locator("button[aria-label='Edit this step']").all()
    txt = btns[14].evaluate("""el => {
        const c = el.closest('div.flex-col, div[data-block-id], section') || el.parentElement;
        return c ? c.innerText : '';
    }""")
    print("\n=== STEP 14 FINAL VALUE ===")
    print(txt.strip())
