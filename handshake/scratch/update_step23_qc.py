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

    # Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # Inspect Step 23
    step23_info = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Edit this step']\"));
        const b23 = btns[23];
        if (!b23) return { error: 'No button 23', total: btns.length };
        
        let card = b23.closest('[data-block-id]') || b23.parentElement;
        return {
            blockId: card ? card.getAttribute('data-block-id') : null,
            text: card ? card.innerText : null
        };
    }""")
    print("Step 23 info before edit:\n", json.dumps(step23_info, indent=2))

    # Click edit on step 23
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Edit this step']\"));
        if (btns[23]) {
            btns[23].scrollIntoView({ behavior: 'instant', block: 'center' });
            btns[23].click();
        }
    }""")
    page.wait_for_timeout(1500)

    # Inspect editor in step 23
    editor_info = page.evaluate("""(reasonText) => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: 'No cancel button found' };
        
        const card = cancelBtn.closest('[data-block-id]') || cancelBtn.parentElement;
        const ta = card.querySelector('textarea, input[type=\"text\"]');
        if (!ta) return { error: 'No textarea in step 23 card' };

        // Fill with reason
        const proto = ta.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
        const nativeSetter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        nativeSetter.call(ta, reasonText);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));

        const subBtn = card.querySelector(\"button[aria-label='Submit']\");
        if (subBtn) {
            subBtn.click();
            return { submitted: true, val: ta.value.slice(0, 50) };
        }
        return { error: 'No submit button in step 23 card' };
    }""", REASON)
    print("Step 23 edit & submit result:\n", json.dumps(editor_info, indent=2))
    page.wait_for_timeout(2000)

    # Click top-bar Save button
    page.evaluate("""() => {
        const topSave = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (topSave && !topSave.disabled) topSave.click();
    }""")
    page.wait_for_timeout(1500)

    # Check Step 23 card text after saving
    step23_after = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Edit this step']\"));
        const b23 = btns[23];
        let card = b23 ? (b23.closest('[data-block-id]') || b23.parentElement) : null;
        return card ? card.innerText : 'None';
    }""")
    print("\nStep 23 card text after edit:\n", step23_after)
