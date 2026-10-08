import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Dismiss timer if visible
    btn = page.locator("button:has-text('Start timer')").first
    if btn.is_visible():
        btn.click()
        page.wait_for_timeout(500)

    # First, let's see what edit button 7 does
    info = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Edit this step']\"));
        const b7 = btns[7];
        if (!b7) return { error: 'No button 7' };
        
        let card = b7.parentElement;
        while (card && !card.getAttribute('data-block-id') && card !== document.body) {
            card = card.parentElement;
        }
        
        return {
            blockId: card ? card.getAttribute('data-block-id') : null,
            cardText: card ? card.innerText : null
        };
    }""")
    print("Step 7 info before click:\n", info)

    # Let's click edit button 7
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Edit this step']\"));
        btns[7].scrollIntoView({ behavior: 'instant', block: 'center' });
        btns[7].click();
    }""")
    page.wait_for_timeout(1500)

    # Now let's inspect the entire DOM of the active editor
    editorInfo = page.evaluate("""() => {
        const activeCard = document.querySelector(\"[data-block-id='9e254568-dd1a-476f-9eb5-d49807d95930']\") || document.querySelector(\"form\") || document.body;
        
        // Find all warnings, callouts, textareas, buttons
        const textareas = Array.from(document.querySelectorAll('textarea')).map(t => ({
            placeholder: t.placeholder,
            value: t.value,
            classes: t.className
        }));
        
        const buttons = Array.from(document.querySelectorAll('button')).filter(b => b.offsetWidth > 0).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            classes: b.className
        }));
        
        // Look for callouts or warning text
        const warnings = Array.from(document.querySelectorAll('*')).filter(el => {
            const t = el.innerText || '';
            return (t.includes('deleted') || t.includes('warning') || t.includes('following blocks')) && el.children.length === 0;
        }).map(el => el.innerText);

        return {
            textareas,
            buttons,
            warnings,
            cardText: activeCard.innerText.slice(0, 1000)
        };
    }""")

    print("\nEditor Info after clicking Edit:")
    print("Warnings:", editorInfo["warnings"])
    print("Textareas:", len(editorInfo["textareas"]))
    for i, t in enumerate(editorInfo["textareas"]):
        print(f"  TA {i}: placeholder={t['placeholder']!r}, value={t['value'][:60]!r}")
    print("Buttons count:", len(editorInfo["buttons"]))
    for b in editorInfo["buttons"]:
        if b["text"] in ["Save", "Cancel", "Submit", "Continue"] or "Submit" in (b["aria"] or ""):
            print(f"  Btn: text={b['text']!r}, aria={b['aria']!r}")

    page.screenshot(path="handshake/scratch/step7_editor_inspected.png")
