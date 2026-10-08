import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const btn = document.querySelector('div.rosetta-card button[aria-label="Continue"]');
            if (!btn) return 'No continue button';
            
            function getFiber(dom) {
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            
            let f = getFiber(btn);
            let onClick = f?.memoizedProps?.onClick;
            return {
                text: btn.innerText,
                type: btn.type,
                onClickStr: onClick ? onClick.toString().slice(0, 1000) : 'None',
                blockId: btn.closest('[data-block-id]')?.getAttribute('data-block-id')
            };
        }''')
        print("Congrats button info:\n", info)

if __name__ == "__main__":
    asyncio.run(main())
