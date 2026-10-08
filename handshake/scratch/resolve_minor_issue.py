import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button", timeout=10000)
    
    # 1. Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)
    
    # 2. Check if Feedback sidebar is open, if not open it
    has_feedback_drawer = page.evaluate("""() => {
        return !!Array.from(document.querySelectorAll('*')).find(el => el.innerText && el.innerText.includes('Minor issue'));
    }""")
    if not has_feedback_drawer:
        print("Opening feedback drawer...")
        page.evaluate("""() => {
            const btn = document.querySelector('button[aria-label=\"Feedback\"]');
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(1500)
        
    # 3. Find and click Resolve on 'Minor issue'
    res = page.evaluate("""() => {
        // Find card with 'Minor issue'
        const headers = Array.from(document.querySelectorAll('span, div, h4, h3')).filter(el => el.innerText && el.innerText.trim() === 'Minor issue');
        if (headers.length === 0) return { error: "Minor issue header not found" };
        
        const card = headers[0].closest('div.border, div.rounded, div.p-4, div.p-3') || headers[0].parentElement.parentElement;
        const resolveBtn = card.querySelector('button[aria-label=\"Resolve\"]');
        if (resolveBtn) {
            resolveBtn.click();
            return { success: true, clicked: "Resolve button on Minor issue" };
        }
        return { error: "No Resolve button on Minor issue card" };
    }""")
    print("Click Minor issue resolve:", res)
    page.wait_for_timeout(2000)
    
    page.screenshot(path="scratch/after_resolve_minor_issue.png")
    
    # 4. Check counter
    cnt = page.evaluate("""() => {
        const m = document.body.innerText.match(/\\d+ \\/ \\d+ items addressed/);
        return m ? m[0] : 'Not found';
    }""")
    print("Counter after Minor issue resolve:", cnt)
