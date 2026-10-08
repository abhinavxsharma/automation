import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # 1. Dismiss timer modal
    page.evaluate("""() => {
        const st = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (st) st.click();
    }""")
    page.wait_for_timeout(1000)
    
    # 2. Check if Error Type edit mode is currently open (look for Cancel button near Error Type)
    # If not open, click the pencil on step 14
    is_open = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        return !!cancelBtn;
    }""")
    print("Is edit mode already open:", is_open)
    
    if not is_open:
        # Click pencil for step 14
        click_edit = page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button[aria-label=\"Edit this step\"]'));
            const target = btns.find(b => {
                const container = b.closest('div.flex-col, div[data-block-id], section') || b.parentElement;
                return container && container.innerText.toLowerCase().includes('error type');
            }) || btns[14];
            if (target) {
                target.scrollIntoView({ behavior: 'instant', block: 'center' });
                target.click();
                return { success: true };
            }
            return { error: "No edit button found" };
        }""")
        print("Click edit result:", click_edit)
        page.wait_for_timeout(1500)
        
    # 3. Select 'Label–element or axis mis-binding'
    select_res = page.evaluate("""() => {
        // Look for any element containing 'Label' and 'mis-binding'
        const all = Array.from(document.querySelectorAll('div, label, span, p, input[type=\"radio\"]'));
        const match = all.find(el => {
            const t = el.innerText || el.textContent || '';
            return t.includes('Label') && t.includes('mis-binding') && t.includes('reads every label correctly');
        });
        
        if (match) {
            match.scrollIntoView({ behavior: 'instant', block: 'center' });
            // Click the element or its parent label/clickable container
            const clickable = match.closest('label, div[role=\"radio\"], div.cursor-pointer') || match;
            clickable.click();
            return { success: true, text: match.innerText ? match.innerText.slice(0, 50) : 'matched' };
        }
        return { error: "Label mis-binding option not found" };
    }""")
    print("Select option result:", select_res)
    page.wait_for_timeout(1000)
    
    # 4. Click the commit arrow button next to Cancel
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
        return { error: "No commit button next to Cancel" };
    }""")
    print("Commit result:", commit_res)
    page.wait_for_timeout(2000)
    
    # 5. Take screenshot
    page.screenshot(path="scratch/step14_fixed.png")
    
    # 6. Verify text of step 14
    txt = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label=\"Edit this step\"]'));
        const target = btns[14];
        if (target) {
            const c = target.closest('div.flex-col, div[data-block-id], section') || target.parentElement;
            return c ? c.innerText : 'Container not found';
        }
        return 'Button 14 not found';
    }""")
    print("\nVerified Step 14 content:")
    print(txt)
