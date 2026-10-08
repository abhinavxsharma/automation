import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    print("--- File inputs ---")
    for fi in pg.locator('input[type="file"]').all():
        print("File input:", fi.evaluate("el => el.outerHTML"))

    print("\n--- Textareas / Text inputs ---")
    for ta in pg.locator("textarea, input[type='text']").all():
        if ta.is_visible():
            print("Tag:", ta.evaluate("el => el.tagName"), "Placeholder:", ta.get_attribute("placeholder"), "Value len:", len(ta.input_value()))

    print("\n--- Checkboxes ---")
    for cb in pg.locator('input[type="checkbox"], [role="checkbox"], label').all():
        if cb.is_visible():
            txt = cb.inner_text().strip()
            if txt and len(txt) < 150:
                print("Checkbox/Label:", repr(txt))

    print("\n--- Buttons ---")
    for b in pg.locator("button").all():
        if b.is_visible():
            txt = b.inner_text().strip()
            if txt:
                print("Button:", repr(txt))
