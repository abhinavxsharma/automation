import sys
sys.path.insert(0, ".")
import time
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx = create_browser_context(p)
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    pg.goto("https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run", timeout=30000)
    time.sleep(3)
    print("Navigated URL:", pg.url)
    print("Title:", pg.title())
    pg.screenshot(path="scratch/check_login.png")
    print("Screenshot saved to scratch/check_login.png")
    body = pg.evaluate("() => document.body ? document.body.innerText.slice(0, 1000) : ''")
    print("Body snippet:")
    print(body[:300])
