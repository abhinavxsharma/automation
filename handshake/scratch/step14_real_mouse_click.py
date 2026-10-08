import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Let's inspect the first radio button
    radio = page.locator("input[type='radio'][value='0']").first
    radio.scroll_into_view_if_needed()
    time.sleep(0.5)

    box = radio.bounding_box()
    print("Radio bounding box:", box)
    if box:
        print(f"Moving mouse to ({box['x'] + box['width']/2}, {box['y'] + box['height']/2}) and clicking...")
        page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
        time.sleep(0.2)
        page.mouse.down()
        time.sleep(0.1)
        page.mouse.up()
        time.sleep(0.5)

    # Also let's click the label right next to it
    label = page.locator("label:has-text('Label–element or axis mis-binding')").first
    lbox = label.bounding_box()
    print("Label bounding box:", lbox)
    if lbox:
        print(f"Clicking label at ({lbox['x'] + 20}, {lbox['y'] + lbox['height']/2})...")
        page.mouse.click(lbox['x'] + 20, lbox['y'] + lbox['height']/2)
        time.sleep(0.5)

    # Now inspect if Continue button is enabled
    cont_btn = page.locator("button:has-text('Continue')").first
    cbox = cont_btn.bounding_box()
    print("Continue button bounding box:", cbox)
    if cbox:
        print("Clicking Continue with mouse...")
        page.mouse.click(cbox['x'] + cbox['width']/2, cbox['y'] + cbox['height']/2)
        time.sleep(2)

    page.screenshot(path="scratch/after_real_mouse_click.png")
    print("Screenshot saved to scratch/after_real_mouse_click.png")
