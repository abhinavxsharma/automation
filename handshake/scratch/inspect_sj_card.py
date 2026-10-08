import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # Inspect the Science Judge card in the sidebar
    sj_card_info = page.evaluate("""() => {
        const sidebar = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.includes('Feedback') && e.innerText.includes('items addressed'));
        if (!sidebar) return { error: "No sidebar found" };

        const cards = Array.from(sidebar.querySelectorAll('div, section, article')).filter(el => {
            return el.innerText && el.innerText.includes('Science Judge - Lumiere');
        });

        // Find smallest container containing Science Judge
        let target = cards[cards.length - 1];

        const allButtonsInSidebar = Array.from(sidebar.querySelectorAll('button')).map((b, idx) => ({
            idx,
            text: b.innerText.trim(),
            ariaLabel: b.getAttribute('aria-label'),
            title: b.getAttribute('title'),
            classes: b.className,
            html: b.outerHTML.substring(0, 150),
            rect: b.getBoundingClientRect()
        }));

        const nextBtn = Array.from(sidebar.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');

        return {
            sidebarText: sidebar.innerText,
            allButtonsInSidebar,
            nextBtnInfo: nextBtn ? {
                text: nextBtn.innerText,
                disabled: nextBtn.disabled,
                classes: nextBtn.className
            } : null
        };
    }""")

    print(json.dumps(sj_card_info, indent=2))
