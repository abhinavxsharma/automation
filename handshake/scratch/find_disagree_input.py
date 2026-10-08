import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    res = pg.evaluate("""() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
        let node;
        const matches = [];
        while ((node = walker.nextNode())) {
            const ph = node.getAttribute('placeholder') || '';
            const txt = node.innerText || '';
            if (ph.toLowerCase().includes('disagree') || txt.toLowerCase().includes('disagree')) {
                matches.push({
                    tag: node.tagName,
                    type: node.getAttribute('type'),
                    ph: ph,
                    text: txt.slice(0, 100),
                    classes: node.className,
                    contentEditable: node.getAttribute('contenteditable'),
                    rect: node.getBoundingClientRect()
                });
            }
        }
        return matches;
    }""")
    print("Matches for disagree:")
    for m in res:
        print(m)
