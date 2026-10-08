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
            function getFiber(dom) {
                if (!dom) return null;
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            
            // Search all elements to find a fiber with taskValuesByBlockId
            let all = Array.from(document.querySelectorAll('*'));
            let store = null;
            for (let el of all) {
                let f = getFiber(el);
                let curr = f;
                while (curr) {
                    if (curr.memoizedState) {
                        let s = curr.memoizedState;
                        while (s) {
                            if (s.memoizedState && typeof s.memoizedState === 'object') {
                                if (s.memoizedState.taskValuesByBlockId) {
                                    store = s.memoizedState;
                                    break;
                                }
                            }
                            s = s.next;
                        }
                    }
                    if (store) break;
                    curr = curr.return;
                }
                if (store) break;
            }
            
            if (!store) {
                // Try finding store from Save button
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
                let bf = getFiber(btn);
                let curr = bf;
                while (curr) {
                    if (curr.memoizedState?.baseQueue || curr.memoizedState?.memoizedState) {
                        let s = curr.memoizedState;
                        while (s) {
                            if (s.memoizedState && typeof s.memoizedState === 'object' && s.memoizedState.getState) {
                                store = s.memoizedState.getState();
                                break;
                            }
                            s = s.next;
                        }
                    }
                    if (store) break;
                    curr = curr.return;
                }
            }
            
            return {
                storeFound: !!store,
                storeKeys: store ? Object.keys(store) : [],
                taskValuesKeys: store?.taskValuesByBlockId ? Object.keys(store.taskValuesByBlockId) : []
            };
        }''')
        print("Store info:", info)

if __name__ == "__main__":
    asyncio.run(main())
