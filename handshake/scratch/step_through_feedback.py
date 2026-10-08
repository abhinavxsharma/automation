import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

REASON_1 = (
    "Added comprehensive justification in the Science Judge section explaining that the flag is an "
    "automated false positive: the Science Judge parser mistakenly quoted the platform checklist label "
    "rather than the actual prompt, which explicitly specifies the CPM critical path calculation and yields the unique answer 76 ms."
)

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    print("Waiting for page readiness...")
    page.wait_for_selector("button:has-text('Save')", timeout=20000)
    page.wait_for_timeout(2000)

    # Dismiss timer modal
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0:
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing Start timer at", box)
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 1. Click Resolve on the first Wageesha card
    print("Clicking first Resolve button...")
    clicked_resolve = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label="Resolve"]'));
        if (btns.length === 0) return { error: "No Resolve button found" };
        btns[0].click();
        return { success: true, count: btns.length };
    }""")
    print("Clicked Resolve:", clicked_resolve)
    page.wait_for_timeout(1500)

    # 2. Inspect what inputs opened in the DOM
    inputs_found = page.evaluate("""() => {
        const inps = Array.from(document.querySelectorAll('input, textarea'));
        return inps.map(i => ({
            tag: i.tagName,
            placeholder: i.placeholder,
            aria: i.getAttribute('aria-label'),
            rect: i.getBoundingClientRect()
        })).filter(i => i.rect.width > 0 && i.rect.height > 0);
    }""")
    print("Visible inputs after clicking Resolve:\n", inputs_found)

    # 3. If there is a resolve input, fill it
    inp_el = page.locator("input[placeholder*='resolve reason'], textarea[placeholder*='resolve reason'], input[placeholder*='Reply'], textarea[placeholder*='Reply']")
    if inp_el.count() > 0:
        print("Found input, filling reason...")
        inp_el.first.fill(REASON_1)
        page.wait_for_timeout(500)

        # Click the send button (the button inside the input's container)
        sent = page.evaluate("""() => {
            const inps = Array.from(document.querySelectorAll("input, textarea")).filter(i => {
                return (i.placeholder.includes('resolve reason') || i.placeholder.includes('Reply')) && i.getBoundingClientRect().width > 0;
            });
            if (inps.length === 0) return { error: "No input found" };
            const container = inps[0].parentElement;
            const btn = container ? container.querySelector('button') : null;
            if (btn) {
                btn.click();
                return { success: true, btnHtml: btn.outerHTML };
            }
            return { error: "No send button in container" };
        }""")
        print("Send click result:", sent)
        page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_first_resolve_submission.png")

    # 4. Check addressed counter
    counter = page.evaluate("""() => {
        const body = document.body.innerText;
        const m = body.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        return m ? m[0] : 'Counter not found';
    }""")
    print("\n--- Addressed Counter ---\n", counter)
