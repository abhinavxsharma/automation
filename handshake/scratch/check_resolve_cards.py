import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button", timeout=10000)
    cards = page.evaluate("""() => {
        const resolveBtns = Array.from(document.querySelectorAll('button[aria-label=\"Resolve\"]'));
        return resolveBtns.map((b, i) => {
            const card = b.closest('div.border, div.rounded, div.p-4, div.p-3, div[class*=\"rosetta\"]') || b.parentElement.parentElement;
            return {
                idx: i,
                cardText: card ? card.innerText : ''
            };
        });
    }""")
    for c in cards:
        print(f"=== RESOLVE BTN {c['idx']} ===")
        print(c['cardText'])
        print()
