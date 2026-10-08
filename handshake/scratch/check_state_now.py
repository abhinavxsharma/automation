import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    # Check for start timer modal and dismiss if present
    modal_text = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const st = btns.find(b => b.innerText.includes('Start timer'));
        if (st) {
            st.click();
            return 'Dismissed start timer';
        }
        return 'No timer modal';
    }""")
    print("Modal check:", modal_text)
    page.wait_for_timeout(1000)

    # Check banner
    banner_info = page.evaluate("""() => {
        const allText = document.body.innerText;
        const bannerLine = allText.split('\\n').find(l => l.includes('sent back') || l.includes('Distractor'));
        return { bannerLine, url: location.href };
    }""")
    print("Banner / URL:", banner_info)

    # Check Distractor #1
    d1_info = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return 'Not found';
        let c = el;
        for (let i = 0; i < 4; i++) if (c.parentElement) c = c.parentElement;
        return {
            text: c.innerText.replace(/\\n/g, ' '),
            hasTextarea: !!c.querySelector('textarea, input[type="text"]'),
            val: c.querySelector('textarea, input[type="text"]')?.value || null
        };
    }""")
    print("Distractor #1:", d1_info)

    # Check feedback sidebar
    fb_info = page.evaluate("""() => {
        const sidebar = Array.from(document.querySelectorAll('div, section, aside')).find(e => e.innerText && e.innerText.includes('Feedback') && e.innerText.includes('items addressed'));
        if (!sidebar) return 'No sidebar found';
        
        // Find buttons in sidebar
        const buttons = Array.from(sidebar.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            ariaLabel: b.getAttribute('aria-label'),
            title: b.getAttribute('title'),
            classes: b.className
        }));
        
        return {
            text: sidebar.innerText,
            buttons: buttons
        };
    }""")
    print("Feedback Sidebar text:\n", fb_info.get("text") if isinstance(fb_info, dict) else fb_info)
    print("Sidebar buttons:", fb_info.get("buttons") if isinstance(fb_info, dict) else [])

    page.screenshot(path="scratch/current_live_inspect.png")
    print("Saved screenshot to scratch/current_live_inspect.png")
