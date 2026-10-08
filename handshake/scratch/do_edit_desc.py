import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Find and click edit on description
    res = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const descHeader = all.find(el => el.innerText && el.innerText.includes('Write a detailed description') && el.children.length === 0);
        if (!descHeader) return { error: "No descHeader" };

        let cur = descHeader;
        while (cur && cur !== document.body) {
            const btn = cur.querySelector('button[aria-label="Edit this step"]');
            if (btn) {
                btn.scrollIntoView({ behavior: 'instant', block: 'center' });
                btn.click();
                return { success: true };
            }
            cur = cur.parentElement;
        }
        return { error: "No edit button found near descHeader" };
    }""")
    print("Click edit result:", res)
    page.wait_for_timeout(1500)

    page.screenshot(path="scratch/live_desc_editor.png")

    info = page.evaluate("""() => {
        const ta = document.querySelector('textarea');
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel' && b.offsetParent !== null);
        let siblings = [];
        if (cancelBtn && cancelBtn.parentElement) {
            siblings = Array.from(cancelBtn.parentElement.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                className: b.className,
                rect: b.getBoundingClientRect()
            }));
        }
        return {
            hasTextarea: !!ta,
            taRect: ta ? ta.getBoundingClientRect() : null,
            hasCancel: !!cancelBtn,
            siblings
        };
    }""")
    print("Editor info:", info)
