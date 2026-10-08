import sys
sys.path.insert(0, ".")
import time
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx = create_browser_context(p)
    pg = next((t for t in ctx.pages if "/task/" in t.url), ctx.pages[0])
    print("Current page title:", pg.title(), pg.url)
    
    # Check Needs attention button
    na_tab = pg.locator("button:has-text('Needs attention')").first
    if na_tab.is_visible(timeout=3000):
        print("Clicking Needs attention...")
        na_tab.click()
        time.sleep(1)
        
    pg.screenshot(path="scratch/needs_attention_verified.png")
    
    cards = pg.locator("div.border.rounded-lg, div[data-testid*='feedback']").all_inner_texts()
    print("Found cards:", len(cards))
    for i, c in enumerate(cards):
        print(f"--- Card {i} ---")
        print(c[:200])
