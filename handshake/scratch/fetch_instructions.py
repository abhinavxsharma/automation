import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, _ = get_page(p)
    page = ctx.new_page()
    page.goto("https://project-lumiere-instructins.learn.joinhandshake.com/", timeout=30000)
    time.sleep(4)
    
    text = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/instructions_page_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    print(f"Instructions fetched! Total chars: {len(text)}")
    print(f"Title: {page.title()}")
    print("Snippet:")
    print(text[:500].encode('ascii', 'replace').decode('ascii'))
