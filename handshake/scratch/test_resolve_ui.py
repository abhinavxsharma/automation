import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # Click first Resolve button
    click_res = pg.evaluate('''() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label="Resolve"]'));
        if (btns.length === 0) return { error: "No resolve buttons" };
        const b = btns[0];
        b.scrollIntoView({ behavior: 'instant', block: 'center' });
        b.click();
        return { success: true, remaining: btns.length };
    }''')
    print("Click Resolve 0:", click_res)
    time.sleep(1.5)
    
    pg.screenshot(path="scratch/after_click_resolve_0.png")
    
    # Inspect what appeared
    info = pg.evaluate('''() => {
        const inputs = Array.from(document.querySelectorAll('textarea, input')).map(i => ({
            tag: i.tagName,
            placeholder: i.placeholder,
            visible: i.getBoundingClientRect().height > 0
        })).filter(i => i.placeholder && i.placeholder.includes('reason'));
        
        const sendBtns = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            svg: !!b.querySelector('svg'),
            visible: b.getBoundingClientRect().height > 0
        })).filter(b => b.visible && (b.aria.includes('Send') || b.text.includes('Send') || b.text.includes('Resolve') || b.aria.includes('Resolve')));

        return { inputs, sendBtns };
    }''')
    print("Inputs found:", info["inputs"])
    print("Send buttons found:", info["sendBtns"])
