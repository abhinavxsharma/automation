import sys, json
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const btn = document.querySelector('button[aria-label="Continue"]');
        const key = Object.keys(btn).find(k => k.startsWith('__reactFiber'));
        let cur = btn[key];
        
        while (cur) {
            if (cur.memoizedProps && cur.memoizedProps.onClick) {
                // Let's inspect scope/closure variables if possible or check window store
                break;
            }
            cur = cur.return;
        }
        
        // Find store in window or react root
        const root = document.querySelector('#__next') || document.body;
        const rootKey = Object.keys(root).find(k => k.startsWith('__reactContainer') || k.startsWith('__reactFiber'));
        return { rootKey };
    }""")
    print("Store inspection:", info)
