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
            let fullStr = onClick ? onClick.toString() : '';
            
            return {
                onClickFull: fullStr
            };
        }''')
        print("onClick source:")
        print(info.get("onClickFull"))

if __name__ == "__main__":
    asyncio.run(main())
