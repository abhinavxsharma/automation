import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, pg = get_task_page(p)
    pg.wait_for_timeout(2000)
    res = pg.evaluate("""() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        const matches = [];
        let node;
        while (node = walker.nextNode()) {
            if (node.nodeValue && node.nodeValue.trim() === 'Exit') {
                const el = node.parentElement;
                matches.push({
                    tagName: el.tagName,
                    outerHTML: el.outerHTML,
                    rect: el.getBoundingClientRect()
                });
            }
        }
        return matches;
    }""")
    print("Found 'Exit' text matches:", len(res))
    for m in res:
        print(m)
