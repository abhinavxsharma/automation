import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # Check if radio option is visible, or click Edit on Error Type if not open
    clicked_option = page.evaluate("""() => {
        // Find label containing 'Label—element or axis mis-binding'
        const all = Array.from(document.querySelectorAll('*'));
        const opt = all.find(e => e.innerText && e.innerText.includes('Label—element or axis mis-binding') && e.children.length === 0);
        if (opt) {
            const target = opt.closest('label') || opt.closest('div[role=\"radio\"]') || opt;
            target.scrollIntoView({ behavior: 'instant', block: 'center' });
            target.click();
            return { success: true, text: opt.innerText };
        }
        return { error: 'Option not found' };
    }""")
    print("Click option result:", clicked_option)
    page.wait_for_timeout(1500)
    
    # If option was clicked, commit it by clicking the arrow button next to Cancel
    commit_res = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button visible" };
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
    
    page.screenshot(path="scratch/after_error_type_committed.png")
    print("Screenshot saved to scratch/after_error_type_committed.png")
