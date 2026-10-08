import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # 1. Dismiss timer modal with mouse
    btn = page.locator("button:has-text('Start timer')").first
    if btn.is_visible():
        box = btn.bounding_box()
        if box:
            print("Dismissing Start timer...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Inspect elements in the right sidebar around x > 900 and y between 200 and 320
    elements_at_icon = page.evaluate("""() => {
        const els = [];
        // Check document.elementFromPoint at several coordinates around the icon
        for (let x = 960; x <= 980; x += 5) {
            for (let y = 260; y <= 275; y += 5) {
                const el = document.elementFromPoint(x, y);
                if (el) {
                    const btn = el.closest('button') || el;
                    els.push({
                        point: { x, y },
                        tag: el.tagName,
                        btnTag: btn.tagName,
                        aria: btn.getAttribute('aria-label'),
                        title: btn.getAttribute('title'),
                        html: btn.outerHTML.substring(0, 100),
                        rect: btn.getBoundingClientRect()
                    });
                }
            }
        }
        return els;
    }""")
    print("Elements at circle-slash icon:\n", json.dumps(elements_at_icon[:4], indent=2))

    # 3. Click the circle-slash button
    clicked_icon = page.evaluate("""() => {
        // Find the button or clickable for circle-slash
        const el = document.elementFromPoint(970, 268);
        if (el) {
            const target = el.closest('button, div[role="button"]') || el;
            target.click();
            return {
                clicked: true,
                tag: target.tagName,
                aria: target.getAttribute('aria-label'),
                rect: target.getBoundingClientRect()
            };
        }
        return { clicked: false };
    }""")
    print("Click circle slash result:", clicked_icon)
    page.wait_for_timeout(1500)

    # 4. Check if any dialog, popover, or textarea appeared
    popups = page.evaluate("""() => {
        const dialog = document.querySelector('div[role="dialog"], [role="alertdialog"], [data-state="open"]');
        const inps = Array.from(document.querySelectorAll('input, textarea')).filter(i => {
            const r = i.getBoundingClientRect();
            return r.width > 0 && r.height > 0 && i.type !== 'radio';
        });
        const allText = document.body.innerText;
        const counter = allText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next' || b.innerText.trim() === 'Submit task');

        return {
            counter: counter ? counter[0] : null,
            btnText: nextBtn ? nextBtn.innerText.trim() : null,
            btnDisabled: nextBtn ? nextBtn.disabled : null,
            visibleInputs: inps.map(i => ({
                tag: i.tagName,
                placeholder: i.placeholder,
                rect: i.getBoundingClientRect()
            })),
            dialogText: dialog ? dialog.innerText.slice(0, 200) : null
        };
    }""")
    print("State after clicking icon:\n", json.dumps(popups, indent=2))

    page.screenshot(path="scratch/after_icon_click_detail.png")
    print("Saved scratch/after_icon_click_detail.png")
