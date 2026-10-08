import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(2000)
    
    btns = page.evaluate("""() => {
        const topNav = document.querySelector('div.flex.h-\\\\[56px\\\\]') || document.querySelector('header') || document.body.firstElementChild;
        const allBtns = Array.from(document.querySelectorAll('button'));
        return allBtns.filter(b => b.getBoundingClientRect().top < 60).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            rect: b.getBoundingClientRect(),
            outerHTML: b.outerHTML.slice(0, 150)
        }));
    }""")
    for i, btn in enumerate(btns):
        print(f"[{i}] {btn}")
