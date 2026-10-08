import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, _ = get_page(p)
    page = ctx.new_page()
    page.goto("https://project-lumiere-instructins.learn.joinhandshake.com/domains", timeout=30000)
    time.sleep(3)
    
    # Dismiss dialog
    page.evaluate('''() => {
        const dialog = document.querySelector('[role="dialog"]');
        if (dialog) {
            const btn = dialog.querySelector('button[aria-label="Close"], button:has(svg), button');
            if (btn) btn.click();
        }
    }''')
    time.sleep(1)
    
    cards = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a, button, [role="button"], div.cursor-pointer')).map(el => ({
            tag: el.tagName,
            text: el.innerText.trim().replace(/\\n/g, ' -- '),
            href: el.href || el.getAttribute('href') || ''
        })).filter(el => el.text.length > 0);
    }''')
    for c in cards:
        print(f"[{c['tag']}] {c['text'].encode('ascii', 'replace').decode('ascii')}: {c['href']}")
