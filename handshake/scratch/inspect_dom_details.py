import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer modal if present
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        print("Dismissing timer modal...")
        page.mouse.click(524, 443)
        page.wait_for_timeout(500)

    print("Frames count:", len(page.frames))
    for fi, f in enumerate(page.frames):
        print(f" Frame {fi}: name='{f.name}' url='{f.url}'")

    res = page.evaluate("""() => {
        const allElements = document.querySelectorAll('*');
        const tags = {};
        for (const el of allElements) {
            tags[el.tagName] = (tags[el.tagName] || 0) + 1;
        }
        
        // Find text content containing 'Golden Solution'
        const golden = Array.from(document.querySelectorAll('*')).filter(el => 
            el.innerText && el.innerText.includes('Golden Solution') && el.children.length === 0
        ).map(el => ({ tag: el.tagName, text: el.innerText, parent: el.parentElement ? el.parentElement.tagName : null }));

        // Find elements near 'Continue'
        const continueBtns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText.includes('Continue')).map(b => ({
            text: b.innerText,
            classes: b.className,
            parent: b.parentElement ? b.parentElement.innerHTML.slice(0, 200) : null
        }));

        return { totalCount: allElements.length, tags, golden, continueBtns };
    }""")
    print("Total DOM elements:", res['totalCount'])
    print("Tags summary:", {k: v for k, v in res['tags'].items() if k in ['DIV', 'BUTTON', 'INPUT', 'TEXTAREA', 'P', 'SPAN', 'FORM']})
    print("Golden matches:", res['golden'])
    print("Continue buttons:", res['continueBtns'])
