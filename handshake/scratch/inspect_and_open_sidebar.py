import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    # Check header buttons
    hdr_info = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('header button, nav button, div button'));
        return btns.map((b, i) => ({
            index: i,
            text: b.innerText.trim(),
            ariaLabel: b.getAttribute('aria-label'),
            title: b.getAttribute('title'),
            html: b.outerHTML.substring(0, 100)
        })).filter(b => b.text || b.ariaLabel || b.title);
    }""")
    print("Header / key buttons:", hdr_info[:15])

    # Open feedback sidebar if not already open
    opened = page.evaluate("""() => {
        const sidebar = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.includes('Feedback') && e.innerText.includes('items addressed'));
        if (sidebar && sidebar.offsetParent !== null) {
            return 'Sidebar already open';
        }
        
        // Find the feedback toggle button in the header
        // It's usually the button next to Tx or with list icon
        const btns = Array.from(document.querySelectorAll('button'));
        const fbToggle = btns.find(b => {
            const aria = b.getAttribute('aria-label') || '';
            const title = b.getAttribute('title') || '';
            return aria.toLowerCase().includes('feedback') || title.toLowerCase().includes('feedback') || b.querySelector('svg path[d*="M4"]');
        });
        
        // Let's also check buttons near 'Save' and 'Exit'
        const saveBtn = btns.find(b => b.innerText.trim() === 'Save');
        const exitBtn = btns.find(b => b.innerText.trim() === 'Exit');
        
        // If there are buttons between Save and Exit:
        if (saveBtn && exitBtn) {
            const allHeaderBtns = btns.filter(b => {
                const rect = b.getBoundingClientRect();
                return rect.top < 60 && rect.right > saveBtn.getBoundingClientRect().right && rect.left < exitBtn.getBoundingClientRect().left;
            });
            // Click the list icon button
            for (const b of allHeaderBtns) {
                if (b !== saveBtn && b !== exitBtn) {
                    b.click();
                    return 'Clicked header button: ' + (b.getAttribute('aria-label') || b.outerHTML.substring(0, 60));
                }
            }
        }
        return 'Could not locate feedback toggle button';
    }""")
    print("Open sidebar attempt:", opened)
    page.wait_for_timeout(1500)

    # Check if sidebar is open now
    fb_text = page.evaluate("""() => {
        const sidebar = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.includes('Feedback') && e.innerText.includes('items addressed'));
        if (!sidebar) return 'Sidebar still not visible';
        return {
            text: sidebar.innerText,
            buttons: Array.from(sidebar.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                title: b.getAttribute('title'),
                classes: b.className
            }))
        };
    }""")
    print("Sidebar state:", fb_text)

    page.screenshot(path="scratch/sidebar_opened_inspect.png")
    print("Screenshot saved to scratch/sidebar_opened_inspect.png")
