import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # 1. Click edit on Step 14
    res = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label=\"Edit this step\"]'));
        const target = btns[14];
        if (!target) return { error: "Button 14 not found" };
        target.scrollIntoView({ behavior: 'instant', block: 'center' });
        target.click();
        return { success: true };
    }""")
    print("Clicked Edit Step 14:", res)
    page.wait_for_timeout(1500)
    
    # 2. Select 'Label–element or axis mis-binding'
    sel_res = page.evaluate("""() => {
        // Find element that contains 'Label' and 'mis-binding'
        // In this form, options are typically inside a list or radio group
        const all = Array.from(document.querySelectorAll('li, div, label, span, p')).filter(el => {
            const t = el.innerText || el.textContent || '';
            return t.includes('Label') && t.includes('mis-binding') && t.includes('reads every label correctly');
        });
        
        // Find the most specific/smallest element that has this text
        all.sort((a, b) => a.innerText.length - b.innerText.length);
        if (all.length > 0) {
            const target = all[0];
            target.scrollIntoView({ behavior: 'instant', block: 'center' });
            target.click();
            return { success: true, text: target.innerText.slice(0, 50) };
        }
        return { error: "Option not found" };
    }""")
    print("Selected Option:", sel_res)
    page.wait_for_timeout(1000)
    
    # 3. Click commit arrow button
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
    
    page.screenshot(path="scratch/step14_after_commit.png")
    
    # Verify Step 14 content
    v_text = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label=\"Edit this step\"]'));
        const target = btns[14];
        if (target) {
            const c = target.closest('div.flex-col, div[data-block-id], section') || target.parentElement;
            return c ? c.innerText : '';
        }
        return '';
    }""")
    print("\nVerified Step 14 text:\n", v_text)
