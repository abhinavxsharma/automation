import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    pg.wait_for_timeout(2000)
    
    # 1. Click Save first to ensure everything is saved
    pg.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const save = btns.find(b => b.innerText && b.innerText.trim() === 'Save');
        if (save) save.click();
    }""")
    print("Clicked Save")
    pg.wait_for_timeout(1000)
    
    # 2. Click top nav Exit button
    exit_clicked = pg.evaluate("""() => {
        const spans = Array.from(document.querySelectorAll('span'));
        const exitSpan = spans.find(s => s.innerText && s.innerText.trim() === 'Exit');
        if (exitSpan) {
            const btn = exitSpan.closest('button');
            if (btn) {
                btn.click();
                return 'Clicked Exit button';
            }
            exitSpan.click();
            return 'Clicked Exit span';
        }
        return 'Exit not found';
    }""")
    print("Exit click:", exit_clicked)
    pg.wait_for_timeout(1500)
    
    # 3. Look for 'Exit task' button in modal
    exit_task_clicked = pg.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const exitTask = btns.find(b => b.innerText && b.innerText.trim().toLowerCase() === 'exit task');
        if (exitTask) {
            exitTask.click();
            return 'Clicked Exit task button';
        }
        return 'Exit task button not found';
    }""")
    print("Exit task click:", exit_task_clicked)
    pg.wait_for_timeout(3000)
    
    pg.screenshot(path="scratch/final_paused_exit_screen.png")
    print("Final URL:", pg.url)
    txt = pg.evaluate("() => document.body ? document.body.innerText : ''")
    print("Final text preview:\n", txt[:400])
