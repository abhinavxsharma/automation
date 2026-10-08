import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Let's inspect the entire feedback list
    feedback_items = page.evaluate("""() => {
        // Collect all items in the feedback panel
        const items = [];
        const panel = document.querySelector('div[class*="overflow-y"]');
        const cards = Array.from(document.querySelectorAll('*')).filter(el => {
            return typeof el.className === 'string' && el.className.includes('border') && (
                el.innerText.includes('Checker') ||
                el.innerText.includes('Judge') ||
                el.innerText.includes('Wageesha') ||
                el.innerText.includes('Finding')
            );
        });

        // Also check Start button
        const startBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Start');
        const startInfo = startBtn ? {
            rect: startBtn.getBoundingClientRect(),
            disabled: startBtn.disabled,
            className: startBtn.className
        } : null;

        // Check all resolve and disagree buttons
        const actionBtns = Array.from(document.querySelectorAll('button')).map((b, i) => {
            const aria = b.getAttribute('aria-label') || '';
            const text = b.innerText.trim();
            const rect = b.getBoundingClientRect();
            return {
                i,
                aria,
                text,
                rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) },
                disabled: b.disabled
            };
        }).filter(b => b.aria || b.text === 'Start');

        return {
            startInfo,
            actionBtns,
            fullFeedbackText: document.body.innerText.slice(document.body.innerText.indexOf('Feedback'))
        };
    }""")

    with open("scratch/feedback_full_items.json", "w", encoding="utf-8") as f:
        json.dump(feedback_items, f, indent=2)

    print("Start button:", feedback_items.get("startInfo"))
    print("\nAction buttons in sidebar:")
    for b in feedback_items.get("actionBtns", []):
        if b['rect']['x'] > 700:
            print(f"  aria='{b['aria']}' text='{b['text']}' rect={b['rect']}")
