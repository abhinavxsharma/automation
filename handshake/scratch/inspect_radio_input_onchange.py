import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const input = document.querySelector('input[type="radio"][value="0"]');
        const key = Object.keys(input).find(k => k.startsWith('__reactFiber'));
        const fiber = input[key];
        
        let res = {};
        if (fiber.memoizedProps && fiber.memoizedProps.onChange) {
            res.inputOnChange = fiber.memoizedProps.onChange.toString();
        }
        
        // Parent component
        let parent = fiber.return;
        while (parent) {
            if (parent.memoizedProps && parent.memoizedProps.onChange) {
                res.parentOnChange = parent.memoizedProps.onChange.toString();
                res.parentName = parent.elementType ? parent.elementType.name : 'anon';
                break;
            }
            parent = parent.return;
        }
        return res;
    }""")
    print("Radio onChange functions:\n")
    print("Input onChange:\n", info.get('inputOnChange', '')[:300])
    print("\nParent onChange:\n", info.get('parentOnChange', '')[:300])
