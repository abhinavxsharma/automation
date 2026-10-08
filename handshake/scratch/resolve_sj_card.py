import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # 1. Dismiss timer modal
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const st = btns.find(b => b.innerText.includes('Start timer'));
        if (st) st.click();
    }""")
    page.wait_for_timeout(1000)

    # 2. Inspect the Science Judge card and all its children/buttons
    card_info = page.evaluate("""() => {
        // Find element with Science Judge - Lumiere
        const matches = Array.from(document.querySelectorAll('*')).filter(el => {
            return el.innerText && el.innerText.includes('Science Judge - Lumiere') && el.children.length > 0;
        });

        // Smallest container
        let card = matches[matches.length - 1];
        while (card && !card.className.includes('border') && card.parentElement && card.parentElement !== document.body) {
            card = card.parentElement;
        }

        const buttons = Array.from(card ? card.querySelectorAll('button') : []).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            title: b.getAttribute('title'),
            classes: b.className,
            html: b.outerHTML.substring(0, 150),
            rect: b.getBoundingClientRect()
        }));

        const svgs = Array.from(card ? card.querySelectorAll('svg') : []).map(s => {
            const r = s.getBoundingClientRect();
            return {
                parentTag: s.parentElement ? s.parentElement.tagName : null,
                parentAria: s.parentElement ? s.parentElement.getAttribute('aria-label') : null,
                rect: { x: r.x, y: r.y, w: r.width, h: r.height }
            };
        });

        return {
            cardTag: card ? card.tagName : null,
            cardClasses: card ? card.className : null,
            cardText: card ? card.innerText : null,
            buttons: buttons,
            svgs: svgs
        };
    }""")
    print("Card info:\n", json.dumps(card_info, indent=2))

    # 3. If there are buttons in the card, click the circle-slash button
    click_res = page.evaluate("""() => {
        // Find the circle-slash button or any button in the Science Judge card
        const cardTextEl = Array.from(document.querySelectorAll('*')).find(el => {
            return el.innerText && el.innerText.includes('Science Judge - Lumiere');
        });
        if (!cardTextEl) return { error: "No SJ card text" };

        let card = cardTextEl;
        while (card && card.parentElement && !card.className.includes('border') && card.parentElement !== document.body) {
            card = card.parentElement;
        }

        const btns = Array.from(card.querySelectorAll('button'));
        if (btns.length > 0) {
            // Click the first button (which is the circle-slash icon)
            const btn = btns[0];
            const r = btn.getBoundingClientRect();
            btn.click();
            return { clicked: true, aria: btn.getAttribute('aria-label'), rect: r, html: btn.outerHTML };
        }

        // What if the icon is not in a <button> but in a clickable div/svg?
        const svgs = Array.from(card.querySelectorAll('svg'));
        if (svgs.length > 0) {
            // Find the one on the top right
            const topSvg = svgs.find(s => s.getBoundingClientRect().x > 900);
            if (topSvg) {
                const target = topSvg.closest('button, div[role="button"], a') || topSvg;
                target.click();
                return { clickedSvg: true, tag: target.tagName, rect: target.getBoundingClientRect() };
            }
        }

        return { error: "No clickable found in card" };
    }""")
    print("Click result:", click_res)
    page.wait_for_timeout(2000)

    # 4. Check if modal / popup / textarea opened, or if status changed to 4/4
    post_click_status = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const counter = bodyText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next' || b.innerText.trim() === 'Submit task');
        const dialog = document.querySelector('div[role="dialog"]');
        
        return {
            counter: counter ? counter[0] : null,
            btnText: nextBtn ? nextBtn.innerText.trim() : null,
            btnDisabled: nextBtn ? nextBtn.disabled : null,
            hasDialog: !!dialog,
            dialogText: dialog ? dialog.innerText : null,
            sidebarText: bodyText.slice(bodyText.indexOf('Feedback'), bodyText.indexOf('Feedback') + 400)
        };
    }""")
    print("Post-click status:\n", json.dumps(post_click_status, indent=2))

    page.screenshot(path="scratch/after_sj_click.png")
    print("Saved scratch/after_sj_click.png")
