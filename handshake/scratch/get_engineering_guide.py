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
        
    btn = page.locator("button:has-text('Engineering and CS')").first
    print("Clicking button:has-text('Engineering and CS')...")
    btn.click()
    time.sleep(4)
    
    print("URL after click:", page.url)
    print("Title after click:", page.title())
    page.screenshot(path="scratch/engineering_guide_page.png")
    
    body = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/engineering_guide_full.txt", "w", encoding="utf-8") as f:
        f.write(body)
    print(f"Saved guide text! Total length: {len(body)}")
    
    # Search for terms
    for term in ["pass", "holding", "rate", "@", "stump", "adversarial"]:
        cnt = body.lower().count(term)
        print(f"Occurrences of '{term}': {cnt}")
