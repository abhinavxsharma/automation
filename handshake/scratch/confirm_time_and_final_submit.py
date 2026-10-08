import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # 1. Click 'Confirm time'
    confirm_res = pg.evaluate('''() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Confirm time');
        if (btn) {
            btn.scrollIntoView({ behavior: 'instant', block: 'center' });
            btn.click();
            return { success: true };
        }
        return { error: "No Confirm time button" };
    }''')
    print("Click Confirm time:", confirm_res)
    time.sleep(3)
    
    pg.screenshot(path="scratch/after_confirm_time.png")
    
    # 2. Check for next button (e.g. 'Submit for review', 'Yes, submit', or similar)
    state = pg.evaluate('''() => {
        const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            classes: b.className
        })).filter(b => b.text || b.aria);
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4')).map(h => h.innerText.trim()).filter(Boolean);
        return {
            url: window.location.href,
            headings,
            buttons,
            bodySnippet: document.body.innerText.slice(0, 1000)
        };
    }''')
    print("Headings:", state["headings"])
    print("Buttons:", state["buttons"])
    print("URL:", state["url"])
    print("Body snippet:\n", state["bodySnippet"][:400])
