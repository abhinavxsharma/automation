import sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    elements = page.evaluate("""() => {
        const matches = [];
        const all = document.querySelectorAll('*');
        for (const el of all) {
            if (el.children.length === 0 && (el.innerText.includes('Jimson') || el.innerText.includes('items addressed') || el.innerText.includes('Image quality issue') || el.innerText.includes('Minor issue'))) {
                matches.push({
                    tag: el.tagName,
                    text: el.innerText.trim(),
                    parentTag: el.parentElement ? el.parentElement.tagName : '',
                    parentCls: el.parentElement ? el.parentElement.className : ''
                });
            }
        }
        return matches;
    }""")
    for m in elements:
        print(m)
