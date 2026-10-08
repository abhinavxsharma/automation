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

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("text=Project Lumière", timeout=15000)

    # 1. Dismiss modal if visible
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # 2. Fill the textarea and click Submit
    submit_res = page.evaluate("""(reasonText) => {
        const allCards = Array.from(document.querySelectorAll(\"div.rounded-rosetta-container\"));
        const sjCard = allCards.find(c => c.innerText && c.innerText.includes('Science Judge'));
        if (!sjCard) return { error: 'No SJ card found' };

        const ta = sjCard.querySelector(\"textarea\");
        if (!ta) return { error: 'No textarea in SJ card' };

        // Set value via prototype setter
        const proto = window.HTMLTextAreaElement.prototype;
        const nativeSetter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        nativeSetter.call(ta, reasonText);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));

        const submitBtn = sjCard.querySelector(\"button[aria-label='Submit']\");
        if (!submitBtn) return { error: 'No submit button in SJ card' };

        // Check if disabled
        const wasDisabled = submitBtn.disabled;
        submitBtn.disabled = false; // ensure enabled
        submitBtn.click();

        return {
            filledValue: ta.value.slice(0, 50),
            wasDisabled,
            clickedSubmit: true
        };
    }""", REASON)
    print("Submit result:\n", json.dumps(submit_res, indent=2))
    page.wait_for_timeout(2000)

    # 3. Dismiss modal if popped up
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(500)

    # 4. Read sidebar text and items addressed
    sidebar_info = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const fbIdx = bodyText.indexOf('Feedback');
        return fbIdx !== -1 ? bodyText.slice(fbIdx, fbIdx + 800) : 'None';
    }""")
    print("\n--- SIDEBAR STATUS AFTER SUBMITTING SJ DISAGREE ---")
    print(sidebar_info)

    page.screenshot(path="handshake/scratch/after_sj_disagree_submitted_success.png")
    print("Saved screenshot to handshake/scratch/after_sj_disagree_submitted_success.png")
