import asyncio
import sys
import json
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        raw_val = await page.evaluate('''() => {
            // Find component fiber on block eac54b4b-5677-48f0-bf86-228cfb012c57
            const el = document.querySelector('[data-block-id="eac54b4b-5677-48f0-bf86-228cfb012c57"]');
            function getFiber(dom) {
                if (!dom) return null;
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            let f = getFiber(el);
            let curr = f;
            let val = null;
            while (curr) {
                if (curr.memoizedProps?.block?.data) {
                    val = curr.memoizedProps.block.data;
                    break;
                }
                if (curr.memoizedProps?.value) {
                    val = curr.memoizedProps.value;
                    break;
                }
                curr = curr.return;
            }
            return { val };
        }''')
        print("Raw value in Fiber:", raw_val)

if __name__ == "__main__":
    asyncio.run(main())
