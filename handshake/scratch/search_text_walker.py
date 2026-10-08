import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    info = page.evaluate("""() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        const matches = [];
        let node;
        while (node = walker.nextNode()) {
            if (node.nodeValue && (node.nodeValue.includes('Jimson') || node.nodeValue.includes('Feedback') || node.nodeValue.includes('Science Judge'))) {
                matches.push({
                    text: node.nodeValue.trim().slice(0, 100),
                    parentTag: node.parentElement.tagName,
                    parentClass: node.parentElement.className,
                    rect: node.parentElement.getBoundingClientRect()
                });
            }
        }
        return matches;
    }""")
    print("Matches found:", len(info))
    for m in info:
        print(m)
