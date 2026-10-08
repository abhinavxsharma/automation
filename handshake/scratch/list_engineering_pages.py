import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, _ = get_page(p)
    page = next((t for t in ctx.pages if "engineering-cs" in t.url), None)
    if not page:
        page = ctx.new_page()
        page.goto("https://project-lumiere-instructins.learn.joinhandshake.com/d/engineering-cs/home", timeout=30000)
        time.sleep(3)
        
    # Dismiss dialog / backdrop if open
    page.evaluate('''() => {
        const backdrops = document.querySelectorAll('div.fixed.inset-0, [role="dialog"]');
        for (const b of backdrops) b.remove();
    }''')
    time.sleep(1)
    
    links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a')).map(a => ({
            text: a.innerText.trim().replace(/\\n/g, ' '),
            href: a.href
        })).filter(a => a.href.includes('/d/engineering-cs/'));
    }''')
    print(f"Total engineering links: {len(links)}")
    seen = set()
    for l in links:
        if l['href'] not in seen:
            seen.add(l['href'])
            print(f"  {l['text'].encode('ascii', 'replace').decode('ascii')}: {l['href']}")
            
    # Also dump all text from home page
    home_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/engineering_home.txt", "w", encoding="utf-8") as f:
        f.write(home_text)
