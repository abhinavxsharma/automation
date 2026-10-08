import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    hierarchy = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const fbHeader = all.find(e => e.innerText && e.innerText.trim() === 'Feedback' && e.children.length === 0);
        if (!fbHeader) return { error: "No Feedback header" };

        let curr = fbHeader;
        const parents = [];
        while (curr && curr !== document.body) {
            parents.push({
                tag: curr.tagName,
                className: curr.className,
                childCount: curr.children.length,
                innerTextSnippet: curr.innerText.slice(0, 150).replace(/\\n/g, ' ')
            });
            curr = curr.parentElement;
        }
        return parents;
    }""")

    print(json.dumps(hierarchy, indent=2))
