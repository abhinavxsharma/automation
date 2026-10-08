import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Dismiss modal if open
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Start timer'));
        if (btn) btn.click();
        const overlays = Array.from(document.querySelectorAll('div[class*="z-50"]'));
        overlays.forEach(o => o.remove());
    }""")
    page.wait_for_timeout(500)

    # Click first Resolve button
    res = page.evaluate("""() => {
        const resolveBtns = Array.from(document.querySelectorAll('button[aria-label="Resolve"]'));
        if (resolveBtns.length === 0) return { error: "No Resolve buttons found" };
        const b = resolveBtns[0];
        b.click();
        return {
            success: true,
            totalResolveBtns: resolveBtns.length
        };
    }""")
    print("Click first Resolve result:", res)
    page.wait_for_timeout(1000)

    page.screenshot(path="scratch/after_first_resolve.png")
    
    # Check feedback text at bottom
    status_text = page.evaluate("""() => {
        const body = document.body.innerText;
        const start = body.indexOf('Feedback');
        return start !== -1 ? body.slice(start, start + 1000) : 'No feedback';
    }""")
    print("Feedback snippet:\n", status_text)
