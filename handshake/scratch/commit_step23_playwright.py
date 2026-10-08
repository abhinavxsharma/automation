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

    # Dismiss timer modal if present
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(500)

    # 1. Fill the textarea using Playwright locator
    ta = page.locator("textarea").first
    print("Found textarea. Old value:", repr(ta.input_value()))
    ta.fill(REASON)
    page.wait_for_timeout(500)
    print("New value set:", repr(ta.input_value()[:50]))

    # 2. Click the submit button inside the editor
    sub_btn = page.locator("button[aria-label='Submit']").first
    print("Submit button visible:", sub_btn.is_visible())
    sub_btn.click()
    page.wait_for_timeout(2000)

    # 3. Click top-bar Save button
    page.evaluate("""() => {
        const topSave = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (topSave && !topSave.disabled) topSave.click();
    }""")
    page.wait_for_timeout(1500)

    # 4. Check Step 23 card text
    step23_text = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Edit this step']\"));
        const b23 = btns[23];
        let card = b23 ? (b23.closest('[data-block-id]') || b23.parentElement) : null;
        return card ? card.innerText : 'None';
    }""")
    print("\n--- STEP 23 CARD TEXT AFTER COMMIT ---\n", step23_text)

    page.screenshot(path="handshake/scratch/step23_committed_success.png")
    print("Saved screenshot to handshake/scratch/step23_committed_success.png")
