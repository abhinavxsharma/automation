import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # Scroll down to Golden Solution
    pg.evaluate('''() => {
        const h = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div, span'))
            .find(el => el.innerText && el.innerText.trim() === 'Golden Solution:');
        if (h) h.scrollIntoView({ behavior: 'instant', block: 'center' });
    }''')
    
    pg.screenshot(path="scratch/step16_render_check.png")
    print("Screenshot saved to scratch/step16_render_check.png")
