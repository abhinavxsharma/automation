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
    page.wait_for_timeout(2000)

    # Click Confirm time button via JS
    clicked_confirm = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Confirm time');
        if (btn) {
            btn.scrollIntoView({ behavior: 'instant', block: 'center' });
            btn.click();
            return { clicked: true, text: btn.innerText.trim() };
        }
        return { clicked: false, error: 'No Confirm time button' };
    }""")
    print("Confirm time click result:\n", json.dumps(clicked_confirm, indent=2))
    page.wait_for_timeout(4000)

    # Inspect final page state
    final_state = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4')).map(h => h.innerText.trim()).filter(Boolean);
        const buttons = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
        return {
            url: window.location.href,
            title: document.title,
            headings,
            buttons,
            snippet: bodyText.slice(0, 1000).replace(/\\n+/g, ' ')
        };
    }""")
    print("\n--- FINAL TASK SUBMISSION STATE ---")
    print(json.dumps(final_state, indent=2))

    page.screenshot(path="handshake/scratch/final_task_submitted_confirmation.png")
    print("\nSaved screenshot to handshake/scratch/final_task_submitted_confirmation.png")
