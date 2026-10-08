import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    res = page.evaluate("""() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        let target = null;
        while ((node = walker.nextNode())) {
            if (node.nodeValue && node.nodeValue.trim() === 'Integer') {
                target = node.parentElement;
                break;
            }
        }
        if (!target) return 'Integer text node not found';
        
        let curr = target;
        const hierarchy = [];
        for (let i = 0; i < 5 && curr; i++) {
            hierarchy.push({
                tag: curr.tagName,
                role: curr.getAttribute('role'),
                cls: curr.className,
                html: curr.outerHTML.slice(0, 150)
            });
            curr = curr.parentElement;
        }
        
        // Click the target
        target.click();
        return { hierarchy };
    }""")
    print("Click result:", res)
    page.wait_for_timeout(1000)
    page.screenshot(path="scratch/after_integer_tree_click.png")
