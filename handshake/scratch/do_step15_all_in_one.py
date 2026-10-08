import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

NEW_JUSTIFICATION = """The model exhibited a label-to-element mis-binding error. The model correctly identified all graph nodes and directed edge connectivity, but mis-bound the numerical latency badges at the planar crossing of directed edges $(C, F)$ and $(D, E)$. Specifically, it swapped their numerical latency labels: it attached the latency of $21\\,\\text{ms}$ (which belongs to directed edge $C \\to F$) to edge $D \\to E$ (which has a true latency of $12\\,\\text{ms}$), and attached $12\\,\\text{ms}$ to $C \\to F$. Consequently, in Step 2 of its topological dynamic programming evaluation, the model calculated the earliest completion time of node $E$ as $L(E) = \\max(44, 40, 36 + 21) = 57\\,\\text{ms}$ instead of the true value $\\max(44, 40, 36 + 12) = 48\\,\\text{ms}$. Propagating this mis-bound label forward, it computed $L(F) = 57 + 8 = 65\\,\\text{ms}$ and $L(T) = 65 + 20 = 85\\,\\text{ms}$, returning an erroneous final answer of $85\\,\\text{ms}$ instead of the ground truth critical path duration of $76\\,\\text{ms}$ (an $11.8\\%$ error)."""

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # 1. Click edit on Model Failure Justification
    res1 = pg.evaluate('''() => {
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div, span'))
            .filter(el => el.innerText && el.innerText.trim() === 'Model Failure Justification');
            
        if (headings.length === 0) return { error: "No heading found" };
        const h = headings[0];
        
        let parent = h.parentElement;
        let btn = null;
        for (let i = 0; i < 5; i++) {
            if (!parent) break;
            btn = parent.querySelector('button[aria-label="Edit this step"]');
            if (btn) break;
            parent = parent.parentElement;
        }
        
        if (!btn) return { error: "No edit button found" };
        btn.scrollIntoView({ behavior: 'instant', block: 'center' });
        btn.click();
        return { success: true };
    }''')
    print("Step 1 (Click edit):", res1)
    time.sleep(2)
    
    # 2. Fill textarea
    res2 = pg.evaluate('''(val) => {
        const ta = document.querySelector('textarea');
        if (!ta) return { error: "No textarea found" };
        ta.scrollIntoView({ behavior: 'instant', block: 'center' });
        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(ta, val);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        return { success: true, valLen: ta.value.length };
    }''', NEW_JUSTIFICATION)
    print("Step 2 (Fill textarea):", res2)
    time.sleep(1)
    
    # 3. Find and click commit button
    res3 = pg.evaluate('''() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button found" };
        const parent = cancelBtn.parentElement;
        const arrowBtn = Array.from(parent.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (arrowBtn) {
            arrowBtn.scrollIntoView({ behavior: 'instant', block: 'center' });
            arrowBtn.click();
            return { success: true };
        }
        return { error: "No arrow button next to Cancel" };
    }''')
    print("Step 3 (Commit arrow):", res3)
    time.sleep(2.5)
    
    pg.screenshot(path="scratch/step15_all_in_one.png")
    
    # Verify Step 15 text in DOM
    text_check = pg.evaluate('''() => {
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div, span'))
            .filter(el => el.innerText && el.innerText.trim() === 'Model Failure Justification');
        if (headings.length === 0) return 'No heading';
        let parent = headings[0].parentElement;
        for (let i = 0; i < 4; i++) {
            if (parent.innerText.length > 100) return parent.innerText;
            parent = parent.parentElement;
        }
        return parent.innerText;
    }''')
    print("\nVerified Step 15 Text:\n", text_check[:400])
