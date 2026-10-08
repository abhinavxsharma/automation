import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

minor_msg = "Updated Error Type to 'Label–element or axis mis-binding' as instructed, and verified model failure justification matches this category."

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("[data-feedback-item-id='a98b7003-0d11-45a9-9af2-8d73fca4b800']", timeout=10000)
    
    # 1. Fill textarea inside a98b7003
    fill_res = page.evaluate("""(msg) => {
        const item = document.querySelector('[data-feedback-item-id=\"a98b7003-0d11-45a9-9af2-8d73fca4b800\"]');
        if (!item) return { error: "Item not found" };
        let ta = item.querySelector('textarea');
        if (!ta) {
            // Click resolve to open it
            const resBtn = item.querySelector('button[aria-label=\"Resolve\"]');
            if (resBtn) resBtn.click();
        }
        ta = item.querySelector('textarea');
        if (!ta) return { error: "Textarea not found after clicking resolve" };
        
        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(ta, msg);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        
        const submitBtn = item.querySelector('button[aria-label=\"Submit\"]');
        return {
            success: true,
            taVal: ta.value,
            submitDisabled: submitBtn ? submitBtn.disabled : null
        };
    }""", minor_msg)
    print("Fill result:", fill_res)
    page.wait_for_timeout(1000)
    
    # 2. Click submit button
    click_res = page.evaluate("""() => {
        const item = document.querySelector('[data-feedback-item-id=\"a98b7003-0d11-45a9-9af2-8d73fca4b800\"]');
        const submitBtn = item.querySelector('button[aria-label=\"Submit\"]');
        if (submitBtn) {
            submitBtn.click();
            return { clicked: true };
        }
        return { error: "No submit button" };
    }""")
    print("Click submit result:", click_res)
    page.wait_for_timeout(2000)
    
    page.screenshot(path="scratch/minor_issue_resolved.png")
    
    # Check counter
    cnt = page.evaluate("""() => {
        const m = document.body.innerText.match(/\\d+ \\/ \\d+ items addressed/);
        return m ? m[0] : 'Not found';
    }""")
    print("Counter after Minor issue resolved:", cnt)
