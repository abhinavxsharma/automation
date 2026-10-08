import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    btns = page.evaluate("""() => {
        const topNav = Array.from(document.querySelectorAll('header, nav, div.sticky, div[class*=\"header\"]')).find(el => el.innerText.includes('Changes saved') || el.innerText.includes('Save'));
        if (!topNav) return [];
        return Array.from(topNav.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            title: b.getAttribute('title') || '',
            cls: b.className,
            svg: b.querySelector('svg')?.outerHTML.slice(0, 100) || '',
            rect: b.getBoundingClientRect()
        }));
    }""")
    print("Found top bar buttons:", len(btns))
    for i, b_item in enumerate(btns):
        print(f"[{i}] {b_item}")
