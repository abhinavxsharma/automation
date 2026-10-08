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
        
    # Dismiss dialog if open
    page.evaluate('''() => {
        const dialog = document.querySelector('[role="dialog"]');
        if (dialog) {
            const btn = dialog.querySelector('button[aria-label="Close"], button:has(svg), button');
            if (btn) btn.click();
        }
    }''')
    time.sleep(1)
    
    # Click Enter Instructions if present
    page.evaluate('''() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Enter Instructions'));
        if (btn) btn.click();
    }''')
    time.sleep(2)
    
    # Click Engineering and CS
    clicked = page.evaluate('''() => {
        const card = Array.from(document.querySelectorAll('a, button, div, h2, h3, p'))
            .find(e => e.innerText && e.innerText.includes('Engineering and CS'));
        if (card) {
            card.click();
            return true;
        }
        return false;
    }''')
    print("Clicked Engineering and CS:", clicked)
    time.sleep(3)
    
    print("New URL:", page.url)
    print("New Title:", page.title())
    text = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/engineering_instructions.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Engineering guide text len: {len(text)}")
    
    # Search for pass
    matches = [line for line in text.splitlines() if "pass" in line.lower() or "holding" in line.lower() or "rate" in line.lower() or "@" in line]
    print(f"Total matching lines: {len(matches)}")
    for m in matches[:30]:
        print("  ", m[:120].encode('ascii', 'replace').decode('ascii'))
