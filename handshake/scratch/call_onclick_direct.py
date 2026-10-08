import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        res = await page.evaluate('''async () => {
            const btn = document.querySelector("div.rosetta-card button[aria-label='Continue']");
            if (!btn) return 'No button';
            
            function getFiber(dom) {
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            
            let f = getFiber(btn);
            let onClick = f?.memoizedProps?.onClick;
            if (!onClick) return 'No onClick prop';
            
            try {
                let ret = await onClick();
                return { success: true, ret: String(ret) };
            } catch (err) {
                return { error: err.message, stack: err.stack };
            }
        }''')
        print("Direct onClick result:", res, flush=True)
        await asyncio.sleep(1.5)
        
        info = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            return {
                text: card ? card.innerText.slice(0, 300).replace(/\\n+/g, ' ') : null,
                blockId: card?.closest('[data-block-id]')?.getAttribute('data-block-id')
            };
        }''')
        print("After direct call:", info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
