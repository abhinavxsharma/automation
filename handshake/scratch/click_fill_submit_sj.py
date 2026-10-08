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

    # 1. Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # 2. Click Disagree on Science Judge (the second Disagree button)
    click_res = page.evaluate("""() => {
        const allBtns = Array.from(document.querySelectorAll('button'));
        const disagreeBtns = allBtns.filter(b => b.getAttribute('aria-label') === 'Disagree');
        // If there's only 1 Disagree button, it's SJ. If there are 2, it's the second one (index 1).
        const targetBtn = disagreeBtns.length > 1 ? disagreeBtns[1] : disagreeBtns[0];
        if (targetBtn) {
            targetBtn.click();
            return { clicked: true, total: disagreeBtns.length };
        }
        return { clicked: false, total: 0 };
    }""")
    print("Click result:", click_res)
    page.wait_for_timeout(1500)

    # 3. Fill textarea and submit
    fill_res = page.evaluate("""(reasonText) => {
        const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing'], textarea\");
        if (!ta) return { error: 'No textarea found' };

        // Fill textarea via native prototype setter
        const proto = window.HTMLTextAreaElement.prototype;
        const nativeSetter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        nativeSetter.call(ta, reasonText);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));

        // Find the submit button
        let cur = ta.parentElement;
        while (cur && cur.querySelectorAll(\"button[aria-label='Submit']\").length === 0 && cur !== document.body) {
            cur = cur.parentElement;
        }
        const subBtn = cur ? cur.querySelector(\"button[aria-label='Submit']\") : null;
        if (!subBtn) {
            // Fallback: any submit button or button in container
            const btns = cur ? Array.from(cur.querySelectorAll('button')) : [];
            return { error: 'No button[aria-label=Submit]', btnsCount: btns.length };
        }

        subBtn.disabled = false;
        subBtn.click();

        return {
            submitted: true,
            valPreview: ta.value.slice(0, 50)
        };
    }""", REASON)
    print("Fill & submit result:\n", json.dumps(fill_res, indent=2))
    page.wait_for_timeout(2500)

    # 4. Check feedback sidebar status
    sidebar_info = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const fbIdx = bodyText.indexOf('Feedback');
        return fbIdx !== -1 ? bodyText.slice(fbIdx, fbIdx + 800) : 'None';
    }""")
    print("\n--- SIDEBAR STATUS ---")
    print(sidebar_info)

    page.screenshot(path="handshake/scratch/after_sj_fill_and_submit.png")
    print("Saved screenshot to handshake/scratch/after_sj_fill_and_submit.png")
