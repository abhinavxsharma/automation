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
        
    # Find all links on the playbook site
    links = page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a')).map(a => ({
            text: a.innerText.trim().replace(/\\n/g, ' '),
            href: a.href
        })).filter(a => a.text.length > 0);
    }''')
    
    print(f"Total links found: {len(links)}")
    for l in links[:30]:
        print(f"  {l['text'].encode('ascii', 'replace').decode('ascii')}: {l['href']}")
