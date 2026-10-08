import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        function search(root) {
            let found = [];
            const all = root.querySelectorAll('*');
            for (const el of all) {
                if (el.shadowRoot) {
                    found = found.concat(search(el.shadowRoot));
                }
                if (el.childNodes) {
                    for (const cn of el.childNodes) {
                        if (cn.nodeType === Node.TEXT_NODE && cn.nodeValue.includes('Wageesha')) {
                            found.push({
                                text: cn.nodeValue.trim(),
                                inShadow: root !== document,
                                parentTag: el.tagName
                            });
                        }
                    }
                }
            }
            return found;
        }
        return search(document);
    }""")

    print("Found:", info)
