import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    pg.wait_for_timeout(1000)
    
    # Check if 'Exit task' button is visible
    print("Step 1: Clicking 'Exit task'...")
    clicked1 = pg.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const b = btns.find(x => x.innerText && x.innerText.trim().toLowerCase() === 'exit task');
        if (b) {
            b.click();
            return true;
        }
        return false;
    }""")
    print("Step 1 result:", clicked1)
    pg.wait_for_timeout(1500)
    
    # Check for 'Save progress & exit'
    print("Step 2: Clicking 'Save progress & exit'...")
    clicked2 = pg.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const b = btns.find(x => x.innerText && x.innerText.trim().toLowerCase().includes('save progress & exit'));
        if (b) {
            b.click();
            return true;
        }
        return false;
    }""")
    print("Step 2 result:", clicked2)
    pg.wait_for_timeout(4000)
    
    pg.screenshot(path="scratch/final_after_full_exit.png")
    print("Final URL:", pg.url)
    txt = pg.evaluate("() => document.body ? document.body.innerText : ''")
    print("Final page preview:\n", txt[:500])
