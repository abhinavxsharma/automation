import sys

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    file_inputs = page.locator("input[type='file']").all()
    print("Found file inputs:", len(file_inputs))
    for i, fi in enumerate(file_inputs):
        print(
            f"File input {i}: visible={fi.is_visible()}, accept={fi.get_attribute('accept')}"
        )
    page.screenshot(path="handshake/scratch/current_after_remove.png")
    print("Saved current_after_remove.png")
