import sys, json
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const radios = Array.from(document.querySelectorAll('input[type="radio"]'));
        const r = radios[0];
        if (!r) return 'No radio';
        const key = Object.keys(r).find(k => k.startsWith('__reactFiber'));
        let cur = r[key];
        
        let path = [];
        while (cur) {
            const name = cur.elementType ? (typeof cur.elementType === 'string' ? cur.elementType : cur.elementType.name || 'Anonymous') : 'Unknown';
            path.push({
                name,
                props: cur.memoizedProps ? Object.keys(cur.memoizedProps) : [],
                state: cur.memoizedState ? (typeof cur.memoizedState === 'object' ? Object.keys(cur.memoizedState) : typeof cur.memoizedState) : null
            });
            cur = cur.return;
        }
        return path;
    }""")
    print("Fiber hierarchy:")
    for p in info[:15]:
        print(" ", p)
