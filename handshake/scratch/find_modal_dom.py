import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # Inspect all elements in document.body
    modal_info = page.evaluate("""() => {
        const results = [];
        // Walk all elements
        const all = document.querySelectorAll('*');
        for (const el of all) {
            if (el.innerText && (el.innerText.includes('Start timer') || el.innerText.includes('Exit task'))) {
                results.push({
                    tagName: el.tagName,
                    id: el.id,
                    className: el.className,
                    text: el.innerText.slice(0, 100),
                    rect: el.getBoundingClientRect(),
                    childCount: el.children.length
                });
            }
        }
        return results;
    }""")
    print("Found matching elements:", len(modal_info))
    for m in modal_info:
        print(m)
