import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from pathlib import Path
from helper import get_page
from playwright.sync_api import sync_playwright

NEW_DIAGRAM = str(Path("scratch/dag_crystal_clear_v3.png").resolve())

with sync_playwright() as p:
    ctx, pg = get_page(p)
    print("Connected to task page:", pg.title())
    
    # 1. Cancel any open editor or modal
    cancel_btn = pg.locator("button:has-text('Cancel')").first
    if cancel_btn.is_visible(timeout=1000):
        print("Canceling current editor...")
        cancel_btn.click(force=True)
        time.sleep(1)
        
    # 2. Click Edit on Step 7
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    print("Clicking Edit on Step 7...")
    edit_btns[7].scroll_into_view_if_needed()
    time.sleep(0.5)
    edit_btns[7].click(force=True)
    time.sleep(2)
    
    # 3. Click Remove on the old image
    rem_btn = pg.locator("button[aria-label='Remove']").first
    if rem_btn.is_visible(timeout=3000):
        print("Clicking Remove button on old image...")
        rem_btn.click(force=True)
        time.sleep(2)
    else:
        print("Remove button not found!")
        
    pg.screenshot(path="scratch/after_click_remove.png")
    
    # 4. Upload new diagram using file chooser on the '+' / upload button
    upload_btn = pg.locator("button[aria-label='Upload files'], button:has-text('+'), button:has(svg path[d*='M12 4v16m8-8H4'])").first
    print("Triggering upload for:", NEW_DIAGRAM)
    with pg.expect_file_chooser() as fc_info:
        upload_btn.click(force=True)
    fc = fc_info.value
    fc.set_files(NEW_DIAGRAM)
    
    print("Waiting 5 seconds for file upload and preview rendering...")
    time.sleep(5)
    
    pg.screenshot(path="scratch/after_upload_preview.png")
    
    # Check if new thumbnail is visible
    thumb_btn = pg.locator("button[aria-label*='View file']").first
    if thumb_btn.is_visible(timeout=3000):
        print("New attached file:", thumb_btn.get_attribute("aria-label"))
    else:
        print("No thumbnail button visible yet!")
        
    # 5. Click the up-arrow Submit button inside the editor
    cancel_btn = pg.locator("button:has-text('Cancel')").first
    parent = cancel_btn.locator("xpath=..")
    submit_btn = parent.locator("button").last
    print("Clicking submit button inside editor...")
    submit_btn.click(force=True)
    
    print("Waiting 4 seconds for save...")
    time.sleep(4)
    
    # Check if Continue button is visible and click it
    cont_btn = pg.locator("button:has-text('Continue')").first
    if cont_btn.is_visible(timeout=3000):
        print("Clicking Continue button...")
        cont_btn.click(force=True)
        time.sleep(2)
        
    pg.screenshot(path="scratch/after_image_swap_complete.png")
    print("Image swap completed!")
