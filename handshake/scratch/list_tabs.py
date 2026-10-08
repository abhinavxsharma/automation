import sys
sys.path.insert(0, ".")
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx = create_browser_context(p)
    print("CDP connected! Number of pages:", len(ctx.pages))
    for i, pg in enumerate(ctx.pages):
        print(f"Page {i}: url='{pg.url}', title='{pg.title()}'")
