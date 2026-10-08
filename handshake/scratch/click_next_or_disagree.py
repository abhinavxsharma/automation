import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # 1. Dismiss timer modal
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing timer modal via center click...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Inspect buttons on the right side
    sidebar_buttons = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button')).filter(b => {
            const r = b.getBoundingClientRect();
            return r.x > 700;
        });
        return btns.map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            title: b.getAttribute('title'),
            disabled: b.disabled,
            ariaDisabled: b.getAttribute('aria-disabled'),
            classes: b.className,
            rect: {
                x: Math.round(b.getBoundingClientRect().x),
                y: Math.round(b.getBoundingClientRect().y),
                w: Math.round(b.getBoundingClientRect().width),
                h: Math.round(b.getBoundingClientRect().height)
            }
        }));
    }""")
    print("Found right-side buttons:")
    for b in sidebar_buttons:
        print(b)

    # 3. First, try clicking the circle-slash button on the Science Judge card if present
    disagree_clicked = page.evaluate("""() => {
        // Find the button with circle-slash or aria-label='Disagree' or aria-label containing 'disagree' or 'ignore'
        const btns = Array.from(document.querySelectorAll('button')).filter(b => b.getBoundingClientRect().x > 700);
        const disagreeBtn = btns.find(b => {
            const aria = (b.getAttribute('aria-label') || '').toLowerCase();
            return aria.includes('disagree') || aria.includes('ignore') || aria.includes('dismiss');
        });
        if (disagreeBtn) {
            disagreeBtn.click();
            return { clicked: true, aria: disagreeBtn.getAttribute('aria-label') };
        }
        return { clicked: false };
    }""")
    print("Disagree button clicked:", disagree_clicked)
    page.wait_for_timeout(1500)

    # 4. If Next button is present, click Next
    next_clicked = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button')).filter(b => b.getBoundingClientRect().x > 700);
        const nextBtn = btns.find(b => b.innerText.trim() === 'Next');
        if (nextBtn) {
            nextBtn.click();
            return true;
        }
        return false;
    }""")
    print("Next button clicked:", next_clicked)
    page.wait_for_timeout(1500)

    # 5. Check sidebar state after actions
    sidebar_after = page.evaluate("""() => {
        const rightEls = Array.from(document.querySelectorAll('*')).filter(el => {
            const r = el.getBoundingClientRect();
            return r.x > 700 && r.width > 200 && r.height > 500;
        });
        const btns = Array.from(document.querySelectorAll('button')).filter(b => b.getBoundingClientRect().x > 700);
        return {
            text: rightEls[0] ? rightEls[0].innerText : "None",
            buttons: btns.map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                disabled: b.disabled,
                ariaDisabled: b.getAttribute('aria-disabled')
            }))
        };
    }""")

    print("\n=== SIDEBAR AFTER ===")
    print("Text:\n", sidebar_after["text"])
    print("\nButtons:")
    for b in sidebar_after["buttons"]:
        print(b)

    page.screenshot(path="handshake/scratch/after_next_click_live.png")
    print("Screenshot saved to handshake/scratch/after_next_click_live.png")
