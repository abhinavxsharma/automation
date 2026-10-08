import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

REASON = (
    "The prompt explicitly instructs to determine the fully simplified Boolean expression for output Q "
    "in terms of inputs A, B, and C from the provided circuit image, and to return the final answer as a single "
    "Boolean expression for Q using standard Boolean notation. The required output Q and simplification "
    "are completely and unambiguously defined from the prompt and the provided circuit topology."
)


def dismiss_modal(page):
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(500)


ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("text=Project Lumière", timeout=15000)

    # 1. Dismiss modal
    dismiss_modal(page)

    # 2. Click the 1 remaining Disagree button
    disagree_btn = page.locator("button[aria-label='Disagree']").first
    print("Disagree button visible:", disagree_btn.is_visible())
    disagree_btn.click()
    page.wait_for_timeout(1000)

    dismiss_modal(page)

    # 3. Locate the reason textarea
    ta = page.locator("textarea[placeholder='Reason for disagreeing']").first
    print("Reason textarea visible:", ta.is_visible())
    ta.fill(REASON)
    page.wait_for_timeout(500)

    dismiss_modal(page)

    # 4. Find all buttons in the form/container
    container_btns = page.evaluate("""() => {
        const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing']\");
        if (!ta) return null;
        let cur = ta.parentElement;
        while (cur && cur.querySelectorAll('button').length === 0 && cur !== document.body) {
            cur = cur.parentElement;
        }
        return Array.from(cur.querySelectorAll('button')).map((b, idx) => ({
            idx,
            text: b.innerText,
            aria: b.getAttribute('aria-label'),
            disabled: b.disabled,
            outerHTML: b.outerHTML
        }));
    }""")
    print("Container buttons:\n", json.dumps(container_btns, indent=2))

    # 5. Click the submit button
    submitted = page.evaluate("""() => {
        const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing']\");
        if (!ta) return false;
        let cur = ta.parentElement;
        while (cur && cur.querySelectorAll('button').length === 0 && cur !== document.body) {
            cur = cur.parentElement;
        }
        const btns = Array.from(cur.querySelectorAll('button'));
        // Find button with SVG or arrow or last button
        if (btns.length > 0) {
            btns[btns.length - 1].click();
            return true;
        }
        return false;
    }""")
    print("Submitted Disagree form:", submitted)
    page.wait_for_timeout(2000)

    dismiss_modal(page)

    # 6. Check the counter and sidebar status
    status = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const fbIdx = bodyText.indexOf('Feedback');
        return fbIdx !== -1 ? bodyText.slice(fbIdx, fbIdx + 600) : 'None';
    }""")
    print("\n--- SIDEBAR STATUS AFTER SUBMITTING SCIENCE JUDGE DISAGREE ---")
    print(status)

    page.screenshot(path="handshake/scratch/after_sj_disagree_complete.png")
    print("Saved screenshot to handshake/scratch/after_sj_disagree_complete.png")
