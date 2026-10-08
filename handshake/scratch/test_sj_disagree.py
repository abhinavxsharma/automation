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
    page.wait_for_selector("text=Project Lumière", timeout=15000)

    # Dismiss timer modal via JS
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # Click 'All' in the feedback panel
    page.evaluate("""() => {
        const allBtns = Array.from(document.querySelectorAll('*')).filter(e => e.innerText && e.innerText.trim() === 'All');
        if (allBtns.length > 0) allBtns[allBtns.length - 1].click();
    }""")
    page.wait_for_timeout(1000)

    # Inspect the Disagree button and its surrounding elements before click
    res = page.evaluate("""() => {
        const btn = document.querySelector(\"button[aria-label='Disagree']\");
        if (!btn) return { error: 'No disagree button' };
        
        // Let's click it!
        btn.click();
        return { clicked: true };
    }""")
    print("Clicked Disagree button:", res)
    page.wait_for_timeout(1500)

    # Inspect what changed in the DOM
    after_info = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        // Find textareas or inputs that appeared
        const inputs = Array.from(document.querySelectorAll('textarea, input[type=\"text\"]')).map(el => ({
            tag: el.tagName,
            placeholder: el.placeholder,
            value: el.value,
            visible: el.offsetWidth > 0
        }));
        
        // Find buttons in the card
        const sjHeading = all.find(e => e.innerText && e.innerText.includes('Science Judge - Lumiere'));
        let card = sjHeading;
        while (card && !card.innerText.includes('Finding number') && card !== document.body) {
            card = card.parentElement;
        }
        if (card && card.parentElement) card = card.parentElement;

        return {
            inputs,
            cardText: card ? card.innerText.slice(0, 1000) : null
        };
    }""")
    print("After Disagree click info:\n", after_info)
    page.screenshot(path="handshake/scratch/after_sj_disagree_click.png")
