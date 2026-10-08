import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
            function getFiber(dom) {
                if (!dom) return null;
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            
            let f = getFiber(btn);
            let curr = f;
            let funcs = [];
            while (curr) {
                if (curr.memoizedState) {
                    let s = curr.memoizedState;
                    while (s) {
                        if (typeof s.memoizedState === 'function') {
                            funcs.push({
                                type: curr.type?.name || 'anon',
                                funcStr: s.memoizedState.toString().slice(0, 300)
                            });
                        }
                        s = s.next;
                    }
                }
                curr = curr.return;
            }
            return funcs;
        }''')
        print(f"Found {len(info)} functions:")
        for fn in info[:10]:
            print(f"- {fn['type']}: {fn['funcStr']}")

if __name__ == "__main__":
    asyncio.run(main())
