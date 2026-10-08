import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(1000)

    # 1. Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0:
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(500)

    # 2. Click edit button on Distractor #1
    print("Clicking edit on Distractor #1...")
    clicked = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return false;
        let c = el;
        while (c && c !== document.body) {
            const btn = c.querySelector('button[aria-label="Edit this step"]');
            if (btn) {
                btn.scrollIntoView({ behavior: 'instant', block: 'center' });
                btn.click();
                return true;
            }
            c = c.parentElement;
        }
        return false;
    }""")
    print("Clicked edit Distractor #1:", clicked)
    page.wait_for_timeout(1000)

    # 3. Locate input/textarea for Distractor #1
    inp = page.locator("input:visible, textarea:visible").first
    print("Visible input count:", inp.count())
    if inp.count() > 0:
        print("Current value:", inp.input_value())
        inp.fill("85")
        page.wait_for_timeout(500)
        print("Updated value to 85.")

        # 4. Click Submit button on step
        submit_btn = page.locator("button[aria-label='Submit']:visible").first
        if submit_btn.count() > 0:
            submit_btn.click(force=True)
            print("Clicked step Submit button.")
            page.wait_for_timeout(1500)

    # 5. Click top Save
    save_btn = page.locator("button:has-text('Save')").first
    if save_btn.is_visible():
        save_btn.click(force=True)
        print("Clicked top Save.")
        page.wait_for_timeout(2000)

    # Check updated value in DOM
    d1_val = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return 'Not found';
        let p = el;
        for (let i = 0; i < 4; i++) if (p.parentElement) p = p.parentElement;
        return p.innerText.replace(/\\n/g, ' ');
    }""")
    print("Updated Distractor #1 in DOM:", d1_val)

    page.screenshot(path="scratch/after_distractor1_fixed.png")
    print("Screenshot saved to scratch/after_distractor1_fixed.png")
