import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    # 1. Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Make sure sidebar is OPEN
    sidebar_status = page.evaluate("""() => {
        let h3 = Array.from(document.querySelectorAll('h3, h2, h4, span, div')).find(e => e.innerText && e.innerText.trim() === 'Feedback');
        const isVisible = (el) => {
            if (!el) return false;
            const r = el.getBoundingClientRect();
            return r.width > 0 && r.height > 0 && el.offsetParent !== null;
        };
        
        let open = isVisible(h3);
        if (!open) {
            // Click feedback toggle
            const fbBtn = document.querySelector('button[aria-label="Feedback"]');
            if (fbBtn) {
                fbBtn.click();
                return 'Clicked feedback toggle to open';
            }
            return 'Feedback toggle button not found';
        }
        return 'Sidebar was already open';
    }""")
    print("Sidebar toggle status:", sidebar_status)
    page.wait_for_timeout(1500)

    # 3. Read sidebar details
    sb_details = page.evaluate("""() => {
        // Find sidebar container
        const h3 = Array.from(document.querySelectorAll('h3, h2, h4, div')).find(e => e.innerText && e.innerText.trim() === 'Feedback');
        if (!h3) return { error: "No feedback header found" };
        
        let container = h3;
        while (container && container.parentElement && container.parentElement !== document.body && container.getBoundingClientRect().width < 350) {
            container = container.parentElement;
        }

        const buttons = Array.from(container.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            title: b.getAttribute('title'),
            classes: b.className
        }));

        return {
            containerText: container.innerText,
            buttons: buttons
        };
    }""")
    print("SIDEBAR DETAILS:\n", json.dumps(sb_details, indent=2))

    # 4. Scroll the main form container to locate Distractor #1
    scroll_res = page.evaluate("""() => {
        // Find scrollable container for the main form
        const containers = Array.from(document.querySelectorAll('div, main')).filter(el => {
            return el.scrollHeight > el.clientHeight + 100 && el.getBoundingClientRect().width > 300;
        });

        // Let's find all elements with 'Distractor' in text
        const d_elements = Array.from(document.querySelectorAll('*')).filter(e => {
            return e.innerText && e.innerText.includes('Distractor #1') && e.children.length < 3;
        });

        // Scroll the element into view if found
        if (d_elements.length > 0) {
            d_elements[0].scrollIntoView({ behavior: 'instant', block: 'center' });
            let p = d_elements[0];
            for (let i = 0; i < 4; i++) if (p.parentElement) p = p.parentElement;
            return {
                found: true,
                cardText: p.innerText.replace(/\\n/g, ' '),
                hasInput: !!p.querySelector('input, textarea'),
                inputVal: p.querySelector('input, textarea')?.value || null,
                buttons: Array.from(p.querySelectorAll('button')).map(b => b.innerText.trim() || b.getAttribute('aria-label'))
            };
        }
        return { found: false, containersCount: containers.length };
    }""")
    print("DISTRACTOR #1 SCROLL & STATUS:\n", json.dumps(scroll_res, indent=2))

    page.screenshot(path="scratch/sidebar_and_d1_inspect.png")
    print("Saved scratch/sidebar_and_d1_inspect.png")
