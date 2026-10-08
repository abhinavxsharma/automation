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
        
    btn = page.locator("text=Enter Instructions").first
    if btn.is_visible(timeout=3000):
        btn.click()
        time.sleep(3)
        
    print("New URL:", page.url)
    print("Title:", page.title())
    
    text = page.evaluate("() => document.body ? document.body.innerText : ''")
    print("Text len:", len(text))
    with open("scratch/playbook_inside.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    # Search for 'pass' or 'holding' or 'rate'
    for line in text.splitlines():
        if any(w in line.lower() for w in ['pass', 'holding', 'rate', 'metric', 'benchmark']):
            print("  Match:", line.encode('ascii', 'replace').decode('ascii'))
