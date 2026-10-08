import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    
    # Find Block 2 answer
    idx2 = text.find("Block 2 Responses:")
    if idx2 != -1:
        b2_snippet = text[idx2:]
        for line in b2_snippet.splitlines()[-30:]:
            print("B2 line:", line.strip().encode('ascii', 'replace').decode('ascii'))
            
    # Click Continue button
    cont_btn = pg.locator("button:has-text('Continue')").last
    if cont_btn.is_visible():
        print("\nClicking Continue button...")
        cont_btn.click()
        time.sleep(3)
    else:
        print("Continue button not visible!")
        
    pg.screenshot(path="scratch/after_b2_continue.png")
    
    # Inspect what steps/inputs are visible now
    new_text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_continue.txt", "w", encoding="utf-8") as f:
        f.write(new_text)
    print(f"\nNew page text length: {len(new_text)}")
    
    # Check for keywords
    for kw in ["Block 1", "Block 2", "Step-by-step", "Final Answer", "Distractor #1", "Distractor #2", "Science Judge"]:
        print(f"Contains '{kw}'? {kw in new_text}")
