import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    res = page.evaluate("""() => {
        const btn = document.querySelector('button[aria-label="Continue"]');
        if (!btn) return 'No continue button with aria-label Continue';
        
        // Find fiber
        const key = Object.keys(btn).find(k => k.startsWith('__reactFiber'));
        if (!key) return 'No fiber on button';
        
        const fiber = btn[key];
        // Traverse up fiber to find form state or props
        let cur = fiber;
        let propsList = [];
        while (cur) {
            if (cur.memoizedProps) {
                const mp = cur.memoizedProps;
                if (mp.onSubmit || mp.onClick || mp.value !== undefined || mp.error) {
                    propsList.push({
                        tag: cur.elementType ? cur.elementType.name || cur.elementType : 'unknown',
                        hasOnSubmit: !!mp.onSubmit,
                        hasOnClick: !!mp.onClick,
                        value: mp.value,
                        error: mp.error
                    });
                }
            }
            cur = cur.return;
        }
        return propsList;
    }""")
    print("Fiber props list:", res)
