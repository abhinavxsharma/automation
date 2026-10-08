import sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    # Check feedback header and items
    fb_header = page.locator("text='Feedback'").first
    print("Feedback header visible:", fb_header.is_visible())
    
    # Check tabs 'All' and 'Needs attention'
    all_tab = page.locator("text='All'").first
    needs_att = page.locator("text='Needs attention'").first
    print("All visible:", all_tab.is_visible(), "Needs attention visible:", needs_att.is_visible())
    
    # Check Jimson cards
    jimson_cards = page.locator("text=Jimson").all()
    print("Jimson cards count:", len(jimson_cards))
    for i, jc in enumerate(jimson_cards):
        parent = jc.locator("xpath=ancestor::div[contains(@class, 'border') or contains(@class, 'rounded')][1]")
        print(f"Card {i} text: {parent.inner_text()}")
        
    # Check bottom counter
    counter = page.locator("text=/\\d+ \\/ \\d+ items addressed/").first
    if counter.is_visible():
        print("Counter:", counter.inner_text())
