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
    page.wait_for_timeout(1000)
    
    # 2. Click Edit on Step 14
    opened = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label=\"Edit this step\"]'));
        // Find Error Type edit button
        const target = btns[14];
        if (target) {
            target.scrollIntoView({ behavior: 'instant', block: 'center' });
            target.click();
            return true;
        }
        return false;
    }""")
    print("Opened Step 14 editor:", opened)
    page.wait_for_timeout(1500)
    
    # 3. Click the label for 'Label–element or axis mis-binding'
    clicked_label = page.evaluate("""() => {
        const labels = Array.from(document.querySelectorAll('label'));
        const target = labels.find(l => l.innerText && l.innerText.trim().startsWith('Label') && l.innerText.includes('mis-binding'));
        if (target) {
            target.scrollIntoView({ behavior: 'instant', block: 'center' });
            target.click();
            
            const inputId = target.getAttribute('for');
            let input = inputId ? document.getElementById(inputId) : target.querySelector('input');
            if (input) input.click();
            
            return { success: true, text: target.innerText.trim() };
        }
        return { error: "Label not found in editor" };
    }""")
    print("Clicked Label:", clicked_label)
    page.wait_for_timeout(1000)
    
    # 4. Click the commit arrow button next to Cancel
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
    page.wait_for_timeout(2500)
    
    page.screenshot(path="scratch/step14_final_check.png")
    
    # 5. Check what is now saved in Step 14
    page.wait_for_selector("button[aria-label='Edit this step']", timeout=10000)
    btns = page.locator("button[aria-label='Edit this step']").all()
    txt = btns[14].evaluate("""el => {
        const c = el.closest('div.flex-col, div[data-block-id], section') || el.parentElement;
        return c ? c.innerText : '';
    }""")
    print("\n=== STEP 14 FINAL VALUE ===")
    print(txt.strip())
