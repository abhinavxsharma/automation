import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button[aria-label='Resolve']", timeout=10000)
    
    # 1. Click Resolve on Image quality issue via JS
    res = page.evaluate("""() => {
        const resolveBtns = Array.from(document.querySelectorAll('button[aria-label=\"Resolve\"]'));
        if (resolveBtns.length > 0) {
            resolveBtns[0].click();
            return { success: true, count: resolveBtns.length };
        }
        return { error: "No resolve button" };
    }""")
    print("Clicked Resolve 0:", res)
    page.wait_for_timeout(2000)
    
    page.screenshot(path="scratch/after_resolve0_clicked.png")
    
    # Check what changed in the UI / counter
    status = page.evaluate("""() => {
        const counter = Array.from(document.querySelectorAll('*')).find(el => el.children.length === 0 && /\\d+ \\/ \\d+ items addressed/.test(el.innerText));
        const inputs = Array.from(document.querySelectorAll('textarea, input')).map(i => ({ val: i.value, ph: i.placeholder }));
        return { counter: counter ? counter.innerText : null, inputs };
    }""")
    print("Status:", status)
