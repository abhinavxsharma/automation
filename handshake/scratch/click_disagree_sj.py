import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button", timeout=10000)
    
    # 1. Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(500)
    
    # 2. Click Disagree on Science Judge
    res = page.evaluate("""() => {
        const disBtn = document.querySelector('button[aria-label=\"Disagree\"]');
        if (disBtn) {
            disBtn.click();
            return { clicked: true };
        }
        return { error: "No Disagree button found" };
    }""")
    print("Clicked Disagree on Science Judge:", res)
    page.wait_for_timeout(1500)
    
    # Check if input opened or if it resolved
    info = page.evaluate("""() => {
        const ta = document.querySelector('textarea[placeholder*=\"reason\"], input[placeholder*=\"reason\"]');
        const counter = document.body.innerText.match(/\\d+ \\/ \\d+ items addressed/);
        return {
            hasTextarea: !!ta,
            ph: ta ? ta.placeholder : null,
            counter: counter ? counter[0] : null
        };
    }""")
    print("State after Disagree click:", info)
    page.screenshot(path="scratch/after_disagree_click.png")
