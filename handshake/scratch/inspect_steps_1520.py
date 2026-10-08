import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button[aria-label='Edit this step']", timeout=10000)
    btns = page.locator("button[aria-label='Edit this step']").all()
    print("Found btns:", len(btns))
    for idx in [7, 11, 14, 15, 18, 19, 20, 21, 22, 23]:
        if idx < len(btns):
            txt = btns[idx].evaluate("""el => {
                const c = el.closest('div.flex-col, div[data-block-id], section') || el.parentElement;
                return c ? c.innerText : '';
            }""")
            print(f"=== STEP {idx} ===")
            print(txt.strip()[:400])
            print("-" * 40)
