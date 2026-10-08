import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

NEW_JUSTIFICATION = """The model exhibited a label-to-element mis-binding error. The model correctly identified all graph nodes and directed edge connectivity, but mis-bound the numerical latency badges at the planar crossing of directed edges $(C, F)$ and $(D, E)$. Specifically, it swapped their numerical latency labels: it attached the latency of $21\\,\\text{ms}$ (which belongs to directed edge $C \\to F$) to edge $D \\to E$ (which has a true latency of $12\\,\\text{ms}$), and attached $12\\,\\text{ms}$ to $C \\to F$. Consequently, in Step 2 of its topological dynamic programming evaluation, the model calculated the earliest completion time of node $E$ as $L(E) = \\max(44, 40, 36 + 21) = 57\\,\\text{ms}$ instead of the true value $\\max(44, 40, 36 + 12) = 48\\,\\text{ms}$. Propagating this mis-bound label forward, it computed $L(F) = 57 + 8 = 65\\,\\text{ms}$ and $L(T) = 65 + 20 = 85\\,\\text{ms}$, returning an erroneous final answer of $85\\,\\text{ms}$ instead of the ground truth critical path duration of $76\\,\\text{ms}$ (an $11.8\\%$ error)."""

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # 1. Fill visible textarea
    fill_res = pg.evaluate("""(val) => {
        const ta = document.querySelector('textarea');
        if (!ta) return { error: "No textarea found" };
        ta.scrollIntoView({ behavior: 'instant', block: 'center' });
        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(ta, val);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        
        // Find buttons in the same container or form
        let parent = ta.parentElement;
        let submitBtn = null;
        for (let i = 0; i < 5; i++) {
            if (!parent) break;
            const btns = Array.from(parent.querySelectorAll('button'));
            submitBtn = btns.find(b => b.innerText.trim() === 'Submit' || b.getAttribute('aria-label') === 'Submit' || (b.querySelector('svg') && !b.innerText.includes('Cancel')));
            if (submitBtn) break;
            parent = parent.parentElement;
        }
        
        if (submitBtn) {
            submitBtn.scrollIntoView({ behavior: 'instant', block: 'center' });
            submitBtn.click();
            return { success: true, clicked: submitBtn.innerText || submitBtn.getAttribute('aria-label') || 'svg button' };
        }
        return { success: true, warning: "Filled textarea but could not find submit button directly" };
    }""", NEW_JUSTIFICATION)
    print("Fill & Commit Step 15:", fill_res)
    time.sleep(2)
    
    pg.screenshot(path="scratch/step15_committed_check.png")
    print("Saved screenshot: scratch/step15_committed_check.png")
