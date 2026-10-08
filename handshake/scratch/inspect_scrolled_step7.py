import sys

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_selector("text=Computer Systems", timeout=15000)

    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print("Total edit buttons:", len(edit_btns))
    if len(edit_btns) > 7:
        edit_btns[7].scroll_into_view_if_needed()
        page.wait_for_timeout(1000)
        page.screenshot(path="handshake/scratch/step7_scrolled_view.png")
        print("Saved step7_scrolled_view.png")

        txt = edit_btns[7].evaluate("""(el) => {
            let p = el.parentElement;
            while (p && p.tagName !== 'BODY') {
                if (p.innerText && p.innerText.includes('Enter your prompt')) {
                    return p.innerText;
                }
                p = p.parentElement;
            }
            return 'not found';
        }""")
        print("Card text:\n", txt[:500])
