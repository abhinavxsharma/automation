import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.screenshot(path="scratch/current_live_edit_state.png")
    txt = page.evaluate("() => document.body ? document.body.innerText : ''")
    idx = txt.find("Error Type")
    if idx != -1:
        print("--- Text around 'Error Type' ---")
        print(txt[idx:idx+1500])
    else:
        print("Error Type not found in text")
