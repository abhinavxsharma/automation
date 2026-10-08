import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const radio0 = document.getElementById('radio-00289b96-5d4f-4efc-821c-14dd0cb7ae0a-0');
            function getFiber(dom) {
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            
            let f = getFiber(radio0);
            let tree = [];
            let curr = f;
            while (curr && tree.length < 30) {
                let typeName = typeof curr.type === 'string' ? curr.type : curr.type?.displayName || curr.type?.name || 'anonymous';
                let propKeys = curr.memoizedProps ? Object.keys(curr.memoizedProps) : [];
                let stateKeys = curr.memoizedState ? Object.keys(curr.memoizedState) : [];
                
                let details = {};
                if (curr.memoizedProps) {
                    for (let k of ['value', 'selected', 'checked', 'onChange', 'onSelect', 'field', 'name', 'id']) {
                        if (k in curr.memoizedProps) details[k] = typeof curr.memoizedProps[k] === 'function' ? 'func' : curr.memoizedProps[k];
                    }
                }
                
                tree.push({
                    type: typeName,
                    details,
                    propKeys: propKeys.slice(0, 10),
                    memoizedState: curr.memoizedState ? (typeof curr.memoizedState === 'object' ? Object.keys(curr.memoizedState) : typeof curr.memoizedState) : null
                });
                curr = curr.return;
            }
            return tree;
        }''')
        print("Fiber Tree:")
        for i, node in enumerate(info):
            print(f"[{i}] {node['type']} - details: {node['details']} - props: {node['propKeys']}")

if __name__ == "__main__":
    asyncio.run(main())
