import asyncio
import sys
import json
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Continue');
            function getFiber(dom) {
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            
            let f = getFiber(btn);
            let onClick = f?.memoizedProps?.onClick;
            
            // Look up the fiber tree for the component that holds ei or taskValues
            let curr = f;
            let found = null;
            while (curr) {
                if (curr.memoizedState) {
                    // inspect hooks
                    let s = curr.memoizedState;
                    while (s) {
                        if (s.memoizedState && typeof s.memoizedState === 'object') {
                            if (s.memoizedState.taskValuesByBlockId || s.memoizedState.pendingTaskValues) {
                                found = s.memoizedState;
                                break;
                            }
                        }
                        s = s.next;
                    }
                }
                if (found) break;
                curr = curr.return;
            }
            
            // Let's also check window or React context
            return {
                found: !!found,
                keys: found ? Object.keys(found) : null
            };
        }''')
        print("Inspection:", info)

if __name__ == "__main__":
    asyncio.run(main())
