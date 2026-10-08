import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # 1. Dismiss timer modal using JS
    print("Dismissing timer modal...")
    dismissed = False
    for _ in range(8):
        res = page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const st = btns.find(b => b.innerText && b.innerText.includes('Start timer'));
            if (st) {
                st.click();
                return true;
            }
            return false;
        }""")
        if res:
            print("Modal dismissed via JS click!")
            dismissed = True
            break
        page.wait_for_timeout(500)
    page.wait_for_timeout(1000)
    
    # 2. Check if Cancel button is already present (editor already open)
    # If not, click Edit this step for Step 14 via JS
    is_editor_open = page.evaluate("""() => {
        return !!Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
    }""")
    print("Is editor open:", is_editor_open)
    
    if not is_editor_open:
        # Click Edit on Step 14
        opened = page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll('button[aria-label=\"Edit this step\"]'));
            // Step 14 is Error Type
            const target = btns.find(b => {
                const c = b.closest('div.flex-col, div[data-block-id], section') || b.parentElement;
                return c && c.innerText.toLowerCase().includes('error type');
            }) || btns[14];
            if (target) {
                target.scrollIntoView({ behavior: 'instant', block: 'center' });
                target.click();
                return true;
            }
            return false;
        }""")
        print("Clicked Edit Step 14 via JS:", opened)
        page.wait_for_timeout(1500)
        
    # 3. Select 'Label–element or axis mis-binding' option
    sel = page.evaluate("""() => {
        // Find text node with 'Label' and 'mis-binding'
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let n, targetNode = null;
        while (n = walker.nextNode()) {
            if (n.nodeValue && n.nodeValue.includes('Label') && n.nodeValue.includes('mis-binding') && n.nodeValue.includes('reads every label correctly')) {
                targetNode = n;
                break;
            }
        }
        if (!targetNode) return { error: "Text node not found" };
        
        let el = targetNode.parentElement;
        // Find closest clickable option (li, label, or div)
        const clickable = el.closest('li, label, div[role=\"radio\"], div[role=\"button\"], div.cursor-pointer') || el;
        clickable.scrollIntoView({ behavior: 'instant', block: 'center' });
        clickable.click();
        return { success: true, tag: clickable.tagName, text: clickable.innerText.slice(0, 50) };
    }""")
    print("Selected Option:", sel)
    page.wait_for_timeout(1000)
    
    # 4. Commit via JS
    committed = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button" };
        const parent = cancelBtn.parentElement;
        const arrowBtn = Array.from(parent.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (arrowBtn) {
            arrowBtn.click();
            return { success: true };
        }
        return { error: "No arrow button" };
    }""")
    print("Committed Step 14:", committed)
    page.wait_for_timeout(2000)
    
    page.screenshot(path="scratch/step14_js_done.png")
    
    # 5. Check what Step 14 shows now
    val = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label=\"Edit this step\"]'));
        const target = btns[14];
        if (target) {
            const c = target.closest('div.flex-col, div[data-block-id], section') || target.parentElement;
            return c ? c.innerText : '';
        }
        return '';
    }""")
    print("\n=== STEP 14 CURRENT DISPLAY ===")
    print(val.strip())
