from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print(f"Total edit buttons: {len(edit_btns)}")

    for i, btn in enumerate(edit_btns):
        # Let's inspect ancestors
        info = btn.evaluate("""el => {
            // Find preceding elements in DOM or parent with header
            let res = {};
            let cur = el;
            let path = [];
            while (cur && cur !== document.body) {
                if (cur.querySelector && cur.querySelector('h1, h2, h3, h4, label')) {
                    const headers = Array.from(cur.querySelectorAll('h1, h2, h3, h4, label')).map(h => h.innerText.trim()).filter(Boolean);
                    if (headers.length > 0) {
                        res.headers = headers;
                        break;
                    }
                }
                cur = cur.parentElement;
            }
            // Also let's find the closest previous heading or text
            let prev = el;
            while (prev && prev.previousElementSibling == null) {
                prev = prev.parentElement;
            }
            if (prev && prev.previousElementSibling) {
                res.prevText = prev.previousElementSibling.innerText.substring(0, 150).replace(/\\n+/g, ' ');
            }
            res.parentText = el.parentElement.innerText.substring(0, 150).replace(/\\n+/g, ' ');
            return res;
        }""")
        print(f"[{i}] headers={info.get('headers', [])[:3]} | prevText='{info.get('prevText', '')[:80]}' | parent='{info.get('parentText', '')[:80]}'")
