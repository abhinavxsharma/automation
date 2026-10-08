import sys, time
sys.path.insert(0, ".")
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx = create_browser_context(p)
    pg = next((t for t in ctx.pages if "/task/" in t.url), None)
    if not pg:
        print("Error: No task page found!")
        sys.exit(1)
        
    print(f"Connected to page: {pg.url}")
    print(f"Page title: {pg.title()}")
    
    # Check for Start timer modal
    modal_btn = pg.locator("button:has-text('Start timer')").first
    if modal_btn.is_visible(timeout=1000):
        print("Start timer modal is visible! Clicking...")
        modal_btn.click()
        time.sleep(1)
    else:
        print("No Start timer modal visible.")

    # Screenshot current view
    pg.screenshot(path="scratch/current_view_state.png", full_page=True)
    print("Full page screenshot saved to scratch/current_view_state.png")

    # Let's inspect all input/textarea/editable elements
    inputs = pg.locator("input, textarea").all()
    print(f"\nTotal inputs/textareas: {len(inputs)}")
    for i, inp in enumerate(inputs):
        try:
            name = inp.get_attribute("name") or ""
            placeholder = inp.get_attribute("placeholder") or ""
            val = inp.input_value()
            val_preview = val[:100].replace('\n', ' ')
            is_disabled = inp.is_disabled()
            print(f"  [{i}] tag={inp.evaluate('e => e.tagName')} name='{name}' placeholder='{placeholder}' disabled={is_disabled} val='{val_preview}'")
        except Exception as e:
            print(f"  [{i}] error: {e}")

    # Inspect all buttons and their text
    buttons = pg.locator("button").all()
    print(f"\nVisible buttons:")
    for b in buttons:
        try:
            if b.is_visible():
                txt = b.inner_text().strip().replace('\n', ' ')
                print(f"  - '{txt}'")
        except Exception:
            pass

    # Inspect sidebar / feedback / alerts
    alerts = pg.locator("[role='alert'], .feedback, [class*='feedback'], [class*='review']").all()
    print(f"\nAlerts / feedback elements: {len(alerts)}")
    for a in alerts:
        try:
            if a.is_visible():
                print(f"  Alert/Feedback: {a.inner_text().strip().replace('\n', ' ')[:200]}")
        except Exception:
            pass
