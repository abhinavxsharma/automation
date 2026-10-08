import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    
    print("Current URL:", page.url)
    # If error screen is still there, click refresh
    err_btn = page.locator("button:has-text('Refresh page')")
    if err_btn.count() > 0:
        print("Clicking Refresh page button...")
        err_btn.click()
        page.wait_for_timeout(2000)

    # Wait for Save button
    print("Waiting for Save button...")
    page.wait_for_selector("button:has-text('Save')", timeout=20000)
    print("Page reloaded successfully!")

    # Check timer modal
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0:
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing Start timer at", box)
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # Check current saved values of description and science judge
    vals = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const descTarget = all.find(e => e.innerText && e.innerText.includes('minimum of 200 words') && e.children.length === 0);
        let descText = '';
        if (descTarget) {
            let c = descTarget;
            for (let i = 0; i < 5; i++) if (c.parentElement) c = c.parentElement;
            descText = c.innerText;
        }

        const sjTarget = all.find(e => e.innerText && e.innerText.includes('Pay close attention to the Science Judge') && e.children.length === 0);
        let sjText = '';
        if (sjTarget) {
            let c = sjTarget;
            for (let i = 0; i < 5; i++) if (c.parentElement) c = c.parentElement;
            sjText = c.innerText;
        }

        const fbStart = document.body.innerText.indexOf('Feedback');
        const fbText = fbStart !== -1 ? document.body.innerText.slice(fbStart, fbStart + 1000) : '';

        return {
            descSnippet: descText.slice(-250),
            descLength: descText.length,
            sjHasJustification: sjText.includes('automated false positive'),
            sjSnippet: sjText.slice(0, 250),
            fbText
        };
    }""")

    print("\n--- Current Saved State ---")
    print("Description length:", vals["descLength"])
    print("Description end snippet:", vals["descSnippet"])
    print("Science Judge has justification?", vals["sjHasJustification"])
    print("Science Judge snippet:", vals["sjSnippet"])
    print("\n--- Feedback Panel ---\n", vals["fbText"])

    page.screenshot(path="scratch/reloaded_check.png")
