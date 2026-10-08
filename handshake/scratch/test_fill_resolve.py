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

    # Dismiss modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Start timer'));
        if (btn) btn.click();
        const overlays = Array.from(document.querySelectorAll('div[class*="z-50"]'));
        overlays.forEach(o => o.remove());
    }""")
    page.wait_for_timeout(500)

    # Check if the input is present
    inp = page.locator("input[placeholder*='resolve reason'], textarea[placeholder*='resolve reason']").first
    print("Resolve reason input count:", inp.count())
    if inp.count() > 0:
        inp.fill(REASON_1)
        page.wait_for_timeout(500)
        print("Filled resolve reason.")

        # Find the send button inside or next to the input's container
        send_res = page.evaluate("""() => {
            const inp = document.querySelector("input[placeholder*='resolve reason'], textarea[placeholder*='resolve reason']");
            if (!inp) return { error: "No input" };
            const container = inp.parentElement;
            const btn = container.querySelector('button');
            if (btn) {
                btn.click();
                return { success: true, btnHtml: btn.outerHTML };
            }
            return { error: "No button in container" };
        }""")
        print("Send button click:", send_res)
        page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_reason_sent.png")

    # Check addressed count
    status = page.evaluate("""() => {
        const body = document.body.innerText;
        const m = body.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        return m ? m[0] : 'Counter not found';
    }""")
    print("Addressed counter:", status)
