import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, _ = get_page(p)
    page = next((t for t in ctx.pages if "project-lumiere-instructins" in t.url), None)
    if not page:
        page = ctx.new_page()
        page.goto("https://project-lumiere-instructins.learn.joinhandshake.com/domains", timeout=30000)
        time.sleep(3)
        
    # 1. Dismiss modal / remove backdrop via JS
    page.evaluate('''() => {
        const backdrops = document.querySelectorAll('div.fixed.inset-0, [role="dialog"]');
        for (const b of backdrops) {
            b.remove();
        }
    }''')
    time.sleep(1)
    
    # 2. Click Engineering and CS button via JS
    clicked = page.evaluate('''() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Engineering and CS'));
        if (btn) {
            btn.click();
            return true;
        }
        return false;
    }''')
    print("Clicked button with JS:", clicked)
    time.sleep(4)
    
    print("New URL:", page.url)
    print("New Title:", page.title())
    body = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/guide_text_loaded.txt", "w", encoding="utf-8") as f:
        f.write(body)
    print("Loaded text length:", len(body))
    
    for line in body.splitlines():
        if any(w in line.lower() for w in ['pass', 'holding', 'rate', 'metric', 'stump', 'target', 'objective', 'fail']):
            print("  ", line[:120].encode('ascii', 'replace').decode('ascii'))
