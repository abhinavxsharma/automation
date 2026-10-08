import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Check text under "Pay close attention to the Science Judge"
    sj_val = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const target = all.find(e => e.innerText && e.innerText.includes('Pay close attention to the Science Judge') && e.children.length === 0);
        if (!target) return 'Target not found';
        let container = target;
        for (let i = 0; i < 5; i++) {
            if (container.parentElement) container = container.parentElement;
        }
        return container.innerText;
    }""")
    print("--- Science Judge Container Text ---\n", sj_val)

    # Check text under "The description should be a minimum of 200 words"
    desc_val = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const target = all.find(e => e.innerText && e.innerText.includes('minimum of 200 words') && e.children.length === 0);
        if (!target) return 'Target not found';
        let container = target;
        for (let i = 0; i < 5; i++) {
            if (container.parentElement) container = container.parentElement;
        }
        return container.innerText;
    }""")
    print("\n--- Description Container Text ---\n", desc_val)
