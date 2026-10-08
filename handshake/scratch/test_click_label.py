import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # 1. Dismiss timer modal if present
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const st = btns.find(b => b.innerText && b.innerText.includes('Start timer'));
        if (st) st.click();
    }""")
    page.wait_for_timeout(500)
    
    # 2. Click the label element starting with 'Label'
    clicked_label = page.evaluate("""() => {
        const labels = Array.from(document.querySelectorAll('label'));
        const target = labels.find(l => l.innerText && l.innerText.trim().startsWith('Label') && l.innerText.includes('mis-binding'));
        if (target) {
            target.scrollIntoView({ behavior: 'instant', block: 'center' });
            target.click();
            
            // Also check if there's an associated input
            const inputId = target.getAttribute('for');
            let input = inputId ? document.getElementById(inputId) : target.querySelector('input');
            if (input) {
                input.click();
            }
            return { success: true, text: target.innerText.trim() };
        }
        return { error: "Label not found" };
    }""")
    print("Clicked Label:", clicked_label)
    page.wait_for_timeout(1000)
    
    # 3. Click the commit arrow button next to Cancel
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
        return { error: "No arrow button" };
    }""")
    print("Commit result:", commit_res)
    page.wait_for_timeout(2000)
    
    page.screenshot(path="scratch/step14_after_label_clicked.png")
    
    # 4. Check Step 14 value
    page.wait_for_selector("button[aria-label='Edit this step']", timeout=10000)
    btns = page.locator("button[aria-label='Edit this step']").all()
    txt = btns[14].evaluate("""el => {
        const c = el.closest('div.flex-col, div[data-block-id], section') || el.parentElement;
        return c ? c.innerText : '';
    }""")
    print("\n=== STEP 14 VERIFIED VALUE ===")
    print(txt.strip())
