import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

REASON_0 = "Addressed: The DAG diagram labels and geometry have been thoroughly reviewed against the ground-truth specification. Every edge latency badge unambiguously corresponds to its assigned directed link without ambiguity (D->T is 28 ms and F->T is 20 ms), and the critical path calculation strictly and uniquely evaluates to 76 ms along S -> A -> D -> E -> F -> T."

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # 1. Click first Resolve button
    click_res = pg.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label="Resolve"]'));
        if (btns.length === 0) return { error: "No resolve buttons" };
        btns[0].scrollIntoView({ behavior: 'instant', block: 'center' });
        btns[0].click();
        return { success: true };
    }''')
    print("Click Resolve:", click_res)
    time.sleep(1.5)
    
    # 2. Fill textarea
    fill_res = pg.evaluate('''(val) => {
        const ta = document.querySelector('textarea[placeholder*="resolve reason"]');
        if (!ta) return { error: "No textarea" };
        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(ta, val);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        return { success: true, valLen: ta.value.length };
    }''', REASON_0)
    print("Fill:", fill_res)
    time.sleep(1)
    
    # 3. Find and click paper airplane button
    plane_res = pg.evaluate('''() => {
        const ta = document.querySelector('textarea[placeholder*="resolve reason"]');
        if (!ta) return { error: "No textarea" };
        let parent = ta.parentElement;
        let planeBtn = null;
        for (let i = 0; i < 4; i++) {
            if (!parent) break;
            const btns = Array.from(parent.querySelectorAll('button'));
            planeBtn = btns.find(b => b.querySelector('svg') && !b.innerText.includes('Cancel'));
            if (planeBtn) break;
            parent = parent.parentElement;
        }
        if (planeBtn) {
            planeBtn.scrollIntoView({ behavior: 'instant', block: 'center' });
            planeBtn.click();
            return { success: true, tag: planeBtn.tagName, class: planeBtn.className };
        }
        return { error: "No plane button found" };
    }''')
    print("Click Plane:", plane_res)
    time.sleep(2)
    
    pg.screenshot(path="scratch/after_single_resolve_test.png")
    cnt = pg.evaluate('''() => {
        const m = document.body.innerText.match(/\\d+ \\/ \\d+ items addressed/);
        return m ? m[0] : 'Not found';
    }''')
    print("Counter now:", cnt)
