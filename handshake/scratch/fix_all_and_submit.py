import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(1000)

    # 1. Dismiss timer modal
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0:
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Fix Distractor #1 to be strictly "85"
    print("Fixing Distractor #1...")
    inp = page.locator("input:visible, textarea:visible").first
    if inp.count() > 0:
        # Clear completely using keyboard and evaluate
        inp.click()
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        inp.fill("85")
        page.wait_for_timeout(500)
        print("Verified Distractor #1 value:", inp.input_value())

        # Click the commit arrow button next to Cancel
        page.evaluate("""() => {
            const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
            if (!cancelBtn) return;
            const parent = cancelBtn.parentElement;
            const arrowBtn = Array.from(parent.querySelectorAll('button')).find(b => b !== cancelBtn);
            if (arrowBtn) arrowBtn.click();
        }""")
        print("Committed Distractor #1.")
        page.wait_for_timeout(1500)

    # 3. Dismiss modal if it popped up
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(500)

    # 4. Check the 4th item in Feedback panel
    # The Science Judge finding has a circle-slash button
    print("Checking Science Judge feedback button...")
    sj_btn_info = page.evaluate("""() => {
        const card = Array.from(document.querySelectorAll('*')).find(el => {
            return el.innerText && el.innerText.includes('Science Judge - Lumiere') && el.innerText.includes('AMBIGUOUS_PROMPT');
        });
        if (!card) return { error: "No SJ card" };
        let p = card;
        while (p && !p.className.includes('border') && p !== document.body) p = p.parentElement;
        const btns = Array.from(p.querySelectorAll('button')).map(b => ({
            aria: b.getAttribute('aria-label'),
            text: b.innerText.trim(),
            rect: b.getBoundingClientRect()
        }));
        return { btns, cardText: p.innerText.slice(0, 200).replace(/\\n/g, ' ') };
    }""")
    print("SJ feedback card info:", sj_btn_info)

    # Click the disagree/resolve button on that card
    clicked_sj = page.evaluate("""() => {
        const card = Array.from(document.querySelectorAll('*')).find(el => {
            return el.innerText && el.innerText.includes('Science Judge - Lumiere') && el.innerText.includes('AMBIGUOUS_PROMPT');
        });
        if (!card) return false;
        let p = card;
        while (p && !p.className.includes('border') && p !== document.body) p = p.parentElement;
        const btn = p.querySelector('button');
        if (btn) {
            btn.click();
            return true;
        }
        return false;
    }""")
    print("Clicked button on SJ card:", clicked_sj)
    page.wait_for_timeout(1500)

    # Check bottom button (Next or Submit)
    bottom_btn = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button')).filter(b => b.getBoundingClientRect().x > 700);
        return btns.map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            disabled: b.disabled
        })).filter(b => b.text || b.aria);
    }""")
    print("Bottom buttons in sidebar:", bottom_btn)

    # If button says Next, click it
    page.evaluate("""() => {
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next' && b.getBoundingClientRect().x > 700);
        if (nextBtn) nextBtn.click();
    }""")
    page.wait_for_timeout(1500)

    # Check counter now
    counter = page.evaluate("""() => {
        const body = document.body.innerText;
        const m = body.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        return m ? m[0] : 'Not found';
    }""")
    print("Counter after actions:", counter)

    # 5. Click top Save
    save_btn = page.locator("button:has-text('Save')").first
    if save_btn.is_visible():
        save_btn.click(force=True)
        print("Clicked top Save.")
        page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_fixes_prepared.png")
    print("Screenshot saved to scratch/after_fixes_prepared.png")
