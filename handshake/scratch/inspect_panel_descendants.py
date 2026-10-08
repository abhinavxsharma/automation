import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    descendants = page.evaluate("""() => {
        const panel = document.querySelector("[data-testid='task-side-panel']");
        if (!panel) return { error: "No panel" };
        
        const all = Array.from(panel.querySelectorAll('*'));
        return all.map(el => {
            const r = el.getBoundingClientRect();
            return {
                tag: el.tagName,
                role: el.getAttribute('role'),
                text: el.innerText ? el.innerText.trim().slice(0, 40) : '',
                aria: el.getAttribute('aria-label'),
                testid: el.getAttribute('data-testid'),
                type: el.getAttribute('type'),
                rect: { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }
            };
        }).filter(el => el.rect.w > 0 && el.rect.h > 0 && (el.tag === 'BUTTON' || el.tag === 'INPUT' || el.role === 'button' || el.aria || el.text.length > 0));
    }""")

    print("Panel descendants count:", len(descendants) if isinstance(descendants, list) else descendants)
    if isinstance(descendants, list):
        for d in descendants:
            print(d)
