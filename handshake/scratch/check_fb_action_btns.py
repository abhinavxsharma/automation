import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # 1. Dismiss timer modal if present
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)
    
    # Check all buttons in the feedback sidebar
    res = page.evaluate("""() => {
        const checkmarks = Array.from(document.querySelectorAll('button[aria-label=\"Resolve\"]'));
        const disagrees = Array.from(document.querySelectorAll('button[aria-label=\"Disagree\"]'));
        return {
            resolves: checkmarks.map((b, i) => ({
                i,
                rect: b.getBoundingClientRect(),
                cardText: b.closest('div.border, div.rounded, div.p-4, div.p-3')?.innerText.slice(0, 80)
            })),
            disagrees: disagrees.map((b, i) => ({
                i,
                rect: b.getBoundingClientRect(),
                cardText: b.closest('div.border, div.rounded, div.p-4, div.p-3')?.innerText.slice(0, 80)
            }))
        };
    }""")
    print("Feedback action buttons:")
    print("Resolves:", res["resolves"])
    print("Disagrees:", res["disagrees"])
