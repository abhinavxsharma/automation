import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer if visible
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const st = btns.find(b => b.innerText.includes('Start timer'));
        if (st) st.click();
    }""")
    page.wait_for_timeout(1000)

    # Inspect all elements near (970, 265)
    elem_info = page.evaluate("""() => {
        const card = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.includes('Science Judge - Lumiere') && e.children.length > 2);
        if (!card) return { error: "No card found" };

        const allInCard = Array.from(card.querySelectorAll('*')).map(el => ({
            tag: el.tagName,
            aria: el.getAttribute('aria-label'),
            title: el.getAttribute('title'),
            classes: el.className,
            html: el.outerHTML.substring(0, 120),
            rect: el.getBoundingClientRect()
        })).filter(e => e.tag === 'BUTTON' || e.aria || (e.rect.x > 950 && e.rect.y < 300));

        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');

        return {
            cardButtons: allInCard,
            nextBtn: nextBtn ? {
                text: nextBtn.innerText.trim(),
                html: nextBtn.outerHTML,
                rect: nextBtn.getBoundingClientRect()
            } : null
        };
    }""")
    print("Element info:\n", json.dumps(elem_info, indent=2))

    # Click the circle-slash button if found
    clicked = page.evaluate("""() => {
        const card = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.includes('Science Judge - Lumiere') && e.children.length > 2);
        if (!card) return 'No card';

        const btns = Array.from(card.querySelectorAll('button'));
        if (btns.length > 0) {
            btns[0].click();
            return 'Clicked card button: ' + (btns[0].getAttribute('aria-label') || btns[0].outerHTML.substring(0, 60));
        }
        return 'No button in card';
    }""")
    print("Card button click result:", clicked)
    page.wait_for_timeout(1500)

    # Check status now
    status_now = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const counter = bodyText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const sub = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        const next = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        return {
            counter: counter ? counter[0] : null,
            hasSubmitTask: !!sub,
            hasNext: !!next,
            sidebarSnippet: bodyText.slice(bodyText.indexOf('Feedback'), bodyText.indexOf('Feedback') + 400)
        };
    }""")
    print("Status now:\n", json.dumps(status_now, indent=2))

    page.screenshot(path="scratch/after_card_btn_click.png")
    print("Saved scratch/after_card_btn_click.png")
