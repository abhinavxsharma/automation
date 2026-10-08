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
            while (curr) {
                let typeName = typeof curr.type === 'string' ? curr.type : curr.type?.displayName || curr.type?.name;
                if (typeName === 'mE') {
                    return {
                        props: Object.keys(curr.memoizedProps || {}),
                        onSave: curr.memoizedProps?.onSave ? curr.memoizedProps.onSave.toString().slice(0, 1000) : null
                    };
                }
                curr = curr.return;
            }
            return 'mE not found';
        }''')
        print("mE info:", info)

if __name__ == "__main__":
    asyncio.run(main())
