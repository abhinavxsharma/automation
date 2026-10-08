import sys, json
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const r = document.querySelector('input[type="radio"]');
        if (!r) return 'No radio';
        const key = Object.keys(r).find(k => k.startsWith('__reactFiber'));
        let cur = r[key];
        let eComp = null;
        while (cur) {
            if (cur.memoizedProps && cur.memoizedProps.config) {
                eComp = cur.memoizedProps;
                break;
            }
            cur = cur.return;
        }
        if (!eComp) return 'No config found';
        return {
            config: eComp.config,
            value: eComp.value
        };
    }""")
    print("Component E config:", json.dumps(info, indent=2))
