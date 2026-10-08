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
    
    # Check Step 16 (Golden Solution)
    btns = page.locator("button[aria-label='Edit this step']").all()
    # Step 16 is Golden Solution
    txt = btns[16].evaluate("""el => {
        const c = el.closest('div.flex-col, div[data-block-id], section') || el.parentElement;
        return c ? c.innerText : '';
    }""")
    print("=== CURRENT STEP 16 ===")
    print(txt.strip())
