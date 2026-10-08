import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

REASON_1 = "Resolved: Updated the image description to a caption-style overview as requested. Corrected node styling to pale yellow circular disks with thin black outlines. Removed repeated prompt statements and removed planar edge crossing lists that pointed models toward crossing points, while maintaining a complete, clear list of all 15 directed edges and their numeric weights (>200 words)."

REASON_2 = "Resolved: Converted all mathematical expressions, node labels, edge identifiers, latencies, formulas, percentages, and intermediate values in both the Golden Solution and Model Failure Justification to strict KaTeX notation (e.g. $14\\,\\text{ms}$, $L(E) = 48\\,\\text{ms}$, $(C, F)$, $D \\to E$). Retained the granular 9-step recurrence structure with one reasoning step per node, and aligned failure justification to the label-to-element mis-binding category."

def resolve_next(pg, reason, label):
    print(f"\n--- Resolving {label} ---")
    # 1. Click first available Resolve button
    click_res = pg.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label="Resolve"]'));
        if (btns.length === 0) return { error: "No resolve buttons remaining" };
        btns[0].scrollIntoView({ behavior: 'instant', block: 'center' });
        btns[0].click();
        return { success: true, count: btns.length };
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
    }''', reason)
    print("Fill:", fill_res)
    time.sleep(1)
    
    # 3. Click paper airplane button
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
            return { success: true };
        }
        return { error: "No plane button found" };
    }''')
    print("Click Plane:", plane_res)
    time.sleep(2.5)

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # Resolve Item 1
    resolve_next(pg, REASON_1, "Image Description")
    
    # Resolve Item 2
    resolve_next(pg, REASON_2, "KaTeX Format")
    
    # Check final counter
    cnt = pg.evaluate('''() => {
        const m = document.body.innerText.match(/\\d+ \\/ \\d+ items addressed/);
        return m ? m[0] : 'Not found';
    }''')
    print(f"\nFinal Counter: {cnt}")
    
    needs_att = pg.evaluate('''() => {
        const na = Array.from(document.querySelectorAll('div, p, span')).some(el => el.innerText && el.innerText.includes('Nothing needs attention'));
        return na;
    }''')
    print(f"Nothing needs attention: {needs_att}")
    
    pg.screenshot(path="scratch/after_all_3_resolved.png")
    print("Saved screenshot to scratch/after_all_3_resolved.png")
