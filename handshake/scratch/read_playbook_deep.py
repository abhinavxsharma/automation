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
        page.goto("https://project-lumiere-instructins.learn.joinhandshake.com/")
        time.sleep(3)
        
    page.screenshot(path="scratch/playbook_screen.png")
    print("Screenshot saved to scratch/playbook_screen.png")
    
    # Dismiss dialog if open
    dialog_text = page.evaluate('''() => {
        const dialog = document.querySelector('[role="dialog"]');
        if (!dialog) return 'No dialog';
        const t = dialog.innerText;
        const closeBtn = dialog.querySelector('button[aria-label="Close"], button:has(svg), button');
        if (closeBtn) closeBtn.click();
        return t;
    }''')
    print("Dialog dismissed:", dialog_text[:200].replace('\n', ' -- '))
    time.sleep(2)
    
    # Click Enter Instructions via JS (no pointer event intercept)
    enter_res = page.evaluate('''() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Enter Instructions'));
        if (btn) {
            btn.click();
            return 'Clicked Enter Instructions';
        }
        return 'Not found';
    }''')
    print("Enter res:", enter_res)
    time.sleep(3)
    
    print("Current URL:", page.url)
    text = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/playbook_full.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Full text length: {len(text)}")
