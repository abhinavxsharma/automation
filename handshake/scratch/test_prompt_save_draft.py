import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

NEW_PROMPT = """Determine the fully simplified Boolean expression for the output Q in terms of the independent inputs A, B, and C from the provided circuit image. The circuit image is the authoritative source for all gate symbols, wire connections, junctions, inversions, and signal paths. Reconstruct the complete circuit topology from the image before simplifying the Boolean logic. Carefully distinguish OR and XOR gates, identify every inversion bubble, and treat wire crossings as connected only when an explicit junction is present. There is exactly one correct answer.

Trace the circuit from A, B, and C through all gates to Q, derive the necessary intermediate Boolean equations, and simplify the final expression completely.

Return the final answer as a single Boolean expression for Q, using standard Boolean notation with no units or extra quantities."""

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("text=Project Lumière", timeout=15000)

    # Dismiss timer modal via JS
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # Open Step 7
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Edit this step']\"));
        if (btns[7]) {
            btns[7].scrollIntoView({ behavior: 'instant', block: 'center' });
            btns[7].click();
        }
    }""")
    page.wait_for_timeout(1500)

    # Fill textarea using native setter
    page.evaluate("""(newVal) => {
        const ta = document.querySelector('textarea');
        if (!ta) return;
        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        nativeSetter.call(ta, newVal);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
    }""", NEW_PROMPT)
    page.wait_for_timeout(500)

    # Check top Save button status
    top_save_info = page.evaluate("""() => {
        const topSave = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        return {
            exists: !!topSave,
            disabled: topSave ? topSave.disabled : null,
            text: topSave ? topSave.innerText : null
        };
    }""")
    print("Top save info while editor open:", top_save_info)

    # Let's see what happens if we click top Save
    if top_save_info["exists"] and not top_save_info["disabled"]:
        page.evaluate("""() => {
            const topSave = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
            topSave.click();
        }""")
        print("Clicked top Save button!")
        page.wait_for_timeout(2000)

    # Now let's see: is editor still open?
    has_cancel = page.evaluate("""() => {
        return !!Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
    }""")
    print("Is editor still open after top Save?", has_cancel)

    # Cancel editor to return to normal
    page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (cancelBtn) cancelBtn.click();
    }""")
    page.wait_for_timeout(1000)

    # Check what Step 7 text is currently rendered in the card
    current_prompt = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Edit this step']\"));
        let p = btns[7].parentElement;
        while (p && !p.getAttribute('data-block-id') && p !== document.body) {
            p = p.parentElement;
        }
        return p ? p.innerText : null;
    }""")
    print("\nRendered prompt in Step 7 card:\n", current_prompt)
