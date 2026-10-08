import sys
import time

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    for _ in range(20):
        t = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Error Type" in t or len(t) > 200:
            break
        time.sleep(0.5)

    # Find all elements with text 'Connectivity / topology error'

    els = page.locator("text='Connectivity / topology error'").all()
    print("Found matching elements:", len(els))
    for i, el in enumerate(els):
        box = el.bounding_box()
        tag = el.evaluate("e => e.tagName")
        parent_tag = el.evaluate("e => e.parentElement.tagName")
        print(f"  El {i}: tag={tag} parent={parent_tag} box={box}")

    if els:
        target = els[-1] # The last one is the radio label
        print("Scrolling target into view and clicking...")
        target.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        target.click(force=True)
        page.wait_for_timeout(500)

        page.screenshot(path="scratch/after_topology_radio_click.png")
        print("Saved scratch/after_topology_radio_click.png")

        cont_btn = page.locator("button:has-text('Continue')").first
        if cont_btn.is_visible():
            print("Clicking Continue...")
            cont_btn.click(force=True)
            page.wait_for_timeout(2000)
            page.screenshot(path="scratch/after_topology_continue.png")
            print("Saved scratch/after_topology_continue.png")

    text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Active Step After Topology Click ---")
    for ln in lines[-35:]:
        print(" ", ln)
