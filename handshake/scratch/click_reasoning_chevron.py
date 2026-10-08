import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    r_btn = pg.locator("button:has-text('Reasoning'), div:has-text('Reasoning')").last
    print("Found reasoning:", r_btn.is_visible())
    r_btn.click()
    time.sleep(1)
    
    pg.screenshot(path="scratch/after_reasoning_click.png")
    
    info = pg.evaluate("""() => {
        const card = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.includes('Science Judge - Lumiere') && e.children.length > 2);
        if (!card) return 'No card';
        return card.innerText;
    }""")
    print("Card text after reasoning click:\n", info)
