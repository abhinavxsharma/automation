import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

minor_msg = "Updated Error Type to 'Label–element or axis mis-binding' as instructed, and verified model failure justification matches this category."
img_msg = "The DAG diagram has been redrawn with every latency badge strictly centered on its own edge trajectory in an open, crossing-free interval with >0.34 clearance to all other edges, completely eliminating badge binding ambiguities. The critical path remains uniquely 76 ms."

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button", timeout=10000)
    
    # 1. Dismiss timer modal
    print("Step 1: Dismissing timer modal...")
    for _ in range(5):
        d = page.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
            if (btn) {
                btn.click();
                return true;
            }
            return false;
        }""")
        if d:
            print("Modal dismissed!")
            break
        page.wait_for_timeout(500)
    page.wait_for_timeout(1000)
    
    # 2. Check if feedback drawer is open
    page.evaluate("""() => {
        const hasCard = Array.from(document.querySelectorAll('*')).some(el => el.innerText && el.innerText.includes('Minor issue'));
        if (!hasCard) {
            const btn = document.querySelector('button[aria-label=\"Feedback\"]');
            if (btn) btn.click();
        }
    }""")
    page.wait_for_timeout(1000)
    
    # 3. Resolve Minor issue
    print("\nStep 2: Resolving Minor issue...")
    res_minor = page.evaluate("""(msg) => {
        const item = document.querySelector('[data-feedback-item-id=\"a98b7003-0d11-45a9-9af2-8d73fca4b800\"]');
        if (!item) return { error: "Minor issue item not found" };
        
        let ta = item.querySelector('textarea');
        if (!ta) {
            const rBtn = item.querySelector('button[aria-label=\"Resolve\"]');
            if (rBtn) rBtn.click();
        }
        return { success: true };
    }""", minor_msg)
    print("Opened resolve on Minor issue:", res_minor)
    page.wait_for_timeout(1500)
    
    fill_minor = page.evaluate("""(msg) => {
        const item = document.querySelector('[data-feedback-item-id=\"a98b7003-0d11-45a9-9af2-8d73fca4b800\"]');
        const ta = item.querySelector('textarea');
        if (!ta) return { error: "No textarea in Minor issue" };
        
        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(ta, msg);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        
        const submitBtn = item.querySelector('button[aria-label=\"Submit\"]');
        if (submitBtn && !submitBtn.disabled) {
            submitBtn.click();
            return { submitted: true };
        }
        return { submitted: false, disabled: submitBtn ? submitBtn.disabled : null };
    }""", minor_msg)
    print("Filled and submitted Minor issue:", fill_minor)
    page.wait_for_timeout(2000)
    
    # 4. Resolve Image quality issue
    print("\nStep 3: Resolving Image quality issue...")
    res_img = page.evaluate("""(msg) => {
        const item = document.querySelector('[data-feedback-item-id=\"ab0fc4a9-6d34-4793-9c2e-afe49805711c\"]');
        if (!item) return { error: "Image quality issue item not found" };
        
        let ta = item.querySelector('textarea');
        if (!ta) {
            const rBtn = item.querySelector('button[aria-label=\"Resolve\"]');
            if (rBtn) rBtn.click();
        }
        return { success: true };
    }""", img_msg)
    print("Opened resolve on Image quality issue:", res_img)
    page.wait_for_timeout(1500)
    
    fill_img = page.evaluate("""(msg) => {
        const item = document.querySelector('[data-feedback-item-id=\"ab0fc4a9-6d34-4793-9c2e-afe49805711c\"]');
        const ta = item.querySelector('textarea');
        if (!ta) return { error: "No textarea in Image quality issue" };
        
        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(ta, msg);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        
        const submitBtn = item.querySelector('button[aria-label=\"Submit\"]');
        if (submitBtn && !submitBtn.disabled) {
            submitBtn.click();
            return { submitted: true };
        }
        return { submitted: false, disabled: submitBtn ? submitBtn.disabled : null };
    }""", img_msg)
    print("Filled and submitted Image quality issue:", fill_img)
    page.wait_for_timeout(2500)
    
    page.screenshot(path="scratch/after_both_resolves.png")
    
    # Check counter
    cnt = page.evaluate("""() => {
        const m = document.body.innerText.match(/\\d+ \\/ \\d+ items addressed/);
        return m ? m[0] : 'Not found';
    }""")
    print("\nCOUNTER AFTER BOTH RESOLVES:", cnt)
