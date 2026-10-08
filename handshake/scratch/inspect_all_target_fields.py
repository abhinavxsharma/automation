import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button", timeout=10000)
    
    # 1. Dismiss timer modal if present
    page.evaluate("""() => {
        const st = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (st) st.click();
    }""")
    page.wait_for_timeout(500)
    
    # Check Step 7 (image attachment)
    img_info = page.evaluate("""() => {
        const imgs = Array.from(document.querySelectorAll('img')).map(img => ({
            src: img.src,
            alt: img.alt,
            width: img.naturalWidth || img.width,
            height: img.naturalHeight || img.height
        }));
        return imgs;
    }""")
    print("Images on page:")
    for im in img_info:
        print(im)
        
    # Check steps 11, 14, 15, 16, 18, 19, 20, 21, 22, 23
    btns = page.locator("button[aria-label='Edit this step']").all()
    print("\nTotal edit buttons:", len(btns))
    for idx in [11, 14, 15, 16, 18, 19, 20, 21, 22, 23]:
        if idx < len(btns):
            txt = btns[idx].evaluate("""el => {
                const c = el.closest('div.flex-col, div[data-block-id], section') || el.parentElement;
                return c ? c.innerText : '';
            }""")
            print(f"\n=== STEP {idx} ===")
            print(txt.strip())
