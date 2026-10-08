import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Find the text input for Final Answer
    text_inputs = page.locator("input[type='text']").all()
    print(f"Total text inputs: {len(text_inputs)}")
    for i, inp in enumerate(text_inputs):
        inp.scroll_into_view_if_needed()
        print(f"[{i}] placeholder='{inp.get_attribute('placeholder')}' value='{inp.input_value()}'")
        
    page.screenshot(path="scratch/final_answer_view.png")
    print("Screenshot saved to scratch/final_answer_view.png")
