import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # 1. Click Submit task
    res = pg.evaluate('''() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        if (!btn) return { error: "No Submit task button found" };
        if (btn.disabled) return { error: "Submit task button is disabled" };
        btn.scrollIntoView({ behavior: 'instant', block: 'center' });
        btn.click();
        return { success: true };
    }''')
    print("Click Submit task:", res)
    time.sleep(3)
    
    pg.screenshot(path="scratch/after_click_submit_now.png")
    print("Screenshot saved to scratch/after_click_submit_now.png")
    
    # Check if a confirmation modal appeared
    modal_info = pg.evaluate('''() => {
        const modalBtns = Array.from(document.querySelectorAll('[role="dialog"] button, [class*="modal"] button, [class*="dialog"] button'))
            .map(b => b.innerText.trim()).filter(Boolean);
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4')).map(h => h.innerText.trim()).filter(Boolean);
        return {
            url: window.location.href,
            headings,
            modalBtns,
            bodySnippet: document.body.innerText.slice(0, 1000)
        };
    }''')
    print("Headings:", modal_info["headings"])
    print("Modal Buttons:", modal_info["modalBtns"])
    print("URL:", modal_info["url"])
    print("Body snippet:\n", modal_info["bodySnippet"][:400])
