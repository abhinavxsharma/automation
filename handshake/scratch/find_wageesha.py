import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const matches = [];
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walker.nextNode())) {
            if (node.nodeValue && node.nodeValue.includes('Wageesha')) {
                const el = node.parentElement;
                matches.push({
                    text: node.nodeValue.trim(),
                    tag: el.tagName,
                    className: el.className,
                    rect: el.getBoundingClientRect()
                });
            }
        }
        return matches;
    }""")

    print("Found Wageesha text nodes:", info)
