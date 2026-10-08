import sys

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible(timeout=1000):
        st.click()
        page.wait_for_timeout(500)

    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print("Total Edit buttons found:", len(edit_btns))
    for i, b in enumerate(edit_btns):
        card_text = page.evaluate(
            """(el) => {
            let parent = el.parentElement;
            for (let k = 0; k < 6; k++) {
                if (!parent) break;
                if (parent.innerText && parent.innerText.length > 20) {
                    return parent.innerText.split('\\n')[0];
                }
                parent = parent.parentElement;
            }
            return 'unknown';
        }""",
            b,
        )
        print(f"Edit button {i}: {card_text}")
