import sys

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_selector("text=Computer Systems", timeout=10000)

    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print("Found Edit buttons:", len(edit_btns))
    for i, b in enumerate(edit_btns):
        near_text = b.evaluate("""(el) => {
            let p = el.parentElement;
            while (p && p !== document.body) {
                if (p.innerText && (p.innerText.includes('prompt') || p.innerText.includes('Determine') || p.innerText.includes('PNG') || p.innerText.includes('lab image'))) {
                    return p.innerText.substring(0, 100).replace(/\\n/g, ' ');
                }
                p = p.parentElement;
            }
            return 'not prompt';
        }""")
        if near_text != "not prompt":
            print(f"Button {i} is near prompt: {near_text}")
        else:
            first_line = b.evaluate("""(el) => {
                let p = el.parentElement;
                while (p && p !== document.body) {
                    if (p.innerText && p.innerText.trim().length > 10) {
                        return p.innerText.trim().split('\\n')[0];
                    }
                    p = p.parentElement;
                }
                return '';
            }""")
            print(f"Button {i}: {first_line}")
