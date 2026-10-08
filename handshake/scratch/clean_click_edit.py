import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(2000)
    
    # 1. Dismiss timer modal if present
    page.evaluate("""() => {
        const st = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (st) st.click();
    }""")
    page.wait_for_timeout(1000)
    
    # 2. Click Error Type edit button (index 14) via JS
    res = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label=\"Edit this step\"]'));
        // Find the button near Error Type
        const target = btns.find(b => {
            const container = b.closest('div.flex-col, div[data-block-id], section') || b.parentElement;
            return container && container.innerText.toLowerCase().includes('error type');
        }) || btns[14];
        
        if (target) {
            target.scrollIntoView({ behavior: 'instant', block: 'center' });
            target.click();
            return { success: true };
        }
        return { error: 'Not found' };
    }""")
    print("JS Click result:", res)
    page.wait_for_timeout(2000)
    page.screenshot(path="scratch/after_js_click_edit_error_type.png")
