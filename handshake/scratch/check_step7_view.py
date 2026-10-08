import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # 1. Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(500)
    
    # 2. Scroll to Step 7 (Prompt / image upload)
    page.wait_for_selector("button[aria-label='Edit this step']", timeout=10000)
    btns = page.locator("button[aria-label='Edit this step']").all()
    # Button 7
    btn7 = btns[7]
    btn7.scroll_into_view_if_needed()
    page.wait_for_timeout(1000)
    
    page.screenshot(path="scratch/step7_scrolled_view.png")
    
    # Check elements inside step 7
    step7_info = btn7.evaluate("""el => {
        const c = el.closest('div.flex-col, div[data-block-id], section') || el.parentElement;
        return {
            text: c ? c.innerText.slice(0, 300) : '',
            hasImg: !!c.querySelector('img'),
            imgSrc: c.querySelector('img')?.src || '',
            hasInputFile: !!c.querySelector('input[type=\"file\"]')
        };
    }""")
    print("Step 7 info:", step7_info)
