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
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        b = st.bounding_box()
        if b:
            page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
            page.wait_for_timeout(1000)

    # Inspect submit button
    sub_info = page.evaluate("""() => {
        const sub = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        if (!sub) return { error: "No Submit task button" };

        const r = sub.getBoundingClientRect();
        return {
            text: sub.innerText.trim(),
            disabled: sub.disabled,
            ariaDisabled: sub.getAttribute('aria-disabled'),
            classes: sub.className,
            rect: { x: r.x, y: r.y, width: r.width, height: r.height },
            html: sub.outerHTML
        };
    }""")
    print("Submit task info:\n", json.dumps(sub_info, indent=2))

    # If it is clickable, let's click it!
    if sub_info.get("ariaDisabled") != "true" and not sub_info.get("disabled"):
        print("Clicking Submit task button...")
        clicked = page.evaluate("""() => {
            const sub = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
            if (sub) {
                sub.click();
                return 'Clicked Submit task';
            }
            return 'Could not click';
        }""")
        print("Result:", clicked)
        page.wait_for_timeout(3000)

        # Inspect any dialog / modal that appeared
        dialog_info = page.evaluate("""() => {
            const dialog = document.querySelector('div[role="dialog"], [role="alertdialog"], div[class*="z-50"]');
            const btns = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
            const allText = document.body.innerText;
            return {
                hasDialog: !!dialog,
                dialogText: dialog ? dialog.innerText : null,
                allButtons: btns.slice(0, 15),
                isReadOnly: allText.includes('read only mode') || allText.includes('Submitted')
            };
        }""")
        print("Dialog info after submit:\n", json.dumps(dialog_info, indent=2))

    page.screenshot(path="scratch/after_submit_attempt.png")
    print("Saved scratch/after_submit_attempt.png")
