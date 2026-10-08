from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    print("Page URL:", page.url)
    print("Page Title:", page.title())
    print("HTML length:", len(page.content()))
    page.screenshot(path="scratch/live_debug.png")
    print("Saved scratch/live_debug.png")
