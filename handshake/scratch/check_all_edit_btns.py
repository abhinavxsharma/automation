import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # Let's count all edit buttons via JS evaluation
    res = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        return btns.map((b, i) => {
            let p = b.parentElement;
            while (p && !p.getAttribute('data-block-id') && !p.className.includes('rounded') && p !== document.body) {
                p = p.parentElement;
            }
            const rect = b.getBoundingClientRect();
            return {
                index: i,
                top: Math.round(rect.top + window.scrollY),
                text: p ? p.innerText.substring(0, 150).replace(/\\n+/g, ' ') : ''
            };
        });
    }""")
    print(f"Total buttons from JS: {len(res)}")
    for r in res:
        print(f"#{r['index']} (y={r['top']}): {r['text'][:100]}")
