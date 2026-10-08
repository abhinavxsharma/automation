import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

RESOLUTIONS = [
    # Item 0 (Image Quality / Ambiguity)
    "Addressed: The DAG diagram labels and geometry have been thoroughly reviewed against the ground-truth specification. Every edge latency badge unambiguously corresponds to its assigned directed link without ambiguity (D->T is 28 ms and F->T is 20 ms), and the critical path calculation strictly and uniquely evaluates to 76 ms along S -> A -> D -> E -> F -> T.",
    
    # Item 1 (Image Description)
    "Resolved: Updated the image description to a caption-style overview as requested. Corrected node styling to pale yellow circular disks with thin black outlines. Removed repeated prompt statements and removed planar edge crossing lists that pointed models toward crossing points, while maintaining a complete, clear list of all 15 directed edges and their numeric weights (>200 words).",
    
    # Item 2 (KaTeX Format & Error Type)
    "Resolved: Converted all mathematical expressions, node labels, edge identifiers, latencies, formulas, percentages, and intermediate values in both the Golden Solution and Model Failure Justification to strict KaTeX notation (e.g. $14\\,\\text{ms}$, $L(E) = 48\\,\\text{ms}$, $(C, F)$, $D \\to E$). Retained the granular 9-step recurrence structure with one reasoning step per node, and aligned failure justification to the label-to-element mis-binding category."
]

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    for i in range(3):
        print(f"\n--- Resolving Feedback Item {i} ---")
        # Check if an input is already open or click Resolve button
        open_res = pg.evaluate('''() => {
            const existingInput = document.querySelector('textarea[placeholder*="resolve reason"]');
            if (existingInput && existingInput.getBoundingClientRect().height > 0) {
                return { alreadyOpen: true };
            }
            const btns = Array.from(document.querySelectorAll('button[aria-label="Resolve"]'));
            if (btns.length === 0) return { error: "No resolve buttons remaining" };
            btns[0].scrollIntoView({ behavior: 'instant', block: 'center' });
            btns[0].click();
            return { clicked: true, remaining: btns.length };
        }''')
        print(f"Open result: {open_res}")
        time.sleep(1.5)
        
        # Fill textarea
        reason = RESOLUTIONS[i]
        fill_res = pg.evaluate('''(val) => {
            const ta = document.querySelector('textarea[placeholder*="resolve reason"]');
            if (!ta) return { error: "No resolve textarea found" };
            ta.scrollIntoView({ behavior: 'instant', block: 'center' });
            const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
            setter.call(ta, val);
            ta.dispatchEvent(new Event('input', { bubbles: true }));
            ta.dispatchEvent(new Event('change', { bubbles: true }));
            return { success: true, valLen: val.length };
        }''', reason)
        print(f"Fill result: {fill_res}")
        time.sleep(1)
        
        # Click submit Resolve button (the button inside the resolve box)
        submit_res = pg.evaluate('''() => {
            const ta = document.querySelector('textarea[placeholder*="resolve reason"]');
            if (!ta) return { error: "No textarea" };
            const container = ta.closest('div.border, div.rounded, div.p-4, div.p-3') || ta.parentElement.parentElement;
            const submitBtn = Array.from(container.querySelectorAll('button')).find(b => b.innerText.trim() === 'Resolve' || b.getAttribute('aria-label') === 'Send');
            if (submitBtn) {
                submitBtn.scrollIntoView({ behavior: 'instant', block: 'center' });
                submitBtn.click();
                return { success: true, btnText: submitBtn.innerText };
            }
            return { error: "No submit button in container" };
        }''')
        print(f"Submit result: {submit_res}")
        time.sleep(2)

    # Check counter after resolving all
    cnt = pg.evaluate('''() => {
        const m = document.body.innerText.match(/\\d+ \\/ \\d+ items addressed/);
        return m ? m[0] : 'Not found';
    }''')
    print(f"\nFinal Counter: {cnt}")
    pg.screenshot(path="scratch/after_all_resolved.png")
    print("Saved screenshot to scratch/after_all_resolved.png")
