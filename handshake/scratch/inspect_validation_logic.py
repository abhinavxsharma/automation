import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const btn = document.querySelector('button[aria-label="Continue"]');
        if (!btn) return 'No continue button';
        const key = Object.keys(btn).find(k => k.startsWith('__reactFiber'));
        let cur = btn[key];
        
        let handlers = [];
        while (cur) {
            if (cur.memoizedProps) {
                if (cur.memoizedProps.onClick) handlers.push({ name: cur.elementType ? cur.elementType.name : 'anon', type: 'onClick', str: cur.memoizedProps.onClick.toString().slice(0, 200) });
                if (cur.memoizedProps.onSubmit) handlers.push({ name: cur.elementType ? cur.elementType.name : 'anon', type: 'onSubmit', str: cur.memoizedProps.onSubmit.toString().slice(0, 200) });
            }
            cur = cur.return;
        }
        return handlers;
    }""")
    print("Handlers:")
    for h in info:
        print(" ", h)
