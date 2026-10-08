import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # 1. Inspect all buttons on page
    buttons = pg.evaluate("""() => {
        return Array.from(document.querySelectorAll('button')).map((b, i) => ({
            i,
            text: b.innerText.trim(),
            ariaLabel: b.getAttribute('aria-label'),
            role: b.getAttribute('role'),
            disabled: b.disabled,
            visible: b.offsetParent !== null,
            className: b.className
        })).filter(b => b.text.length > 0 || b.ariaLabel);
    }""")
    print("=== BUTTONS ON PAGE ===")
    for b in buttons:
        print(b)
        
    pg.screenshot(path="scratch/final_page_state.png")
