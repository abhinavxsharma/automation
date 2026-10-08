import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click Continue on the congrats card
        res = await page.evaluate('''async () => {
            const card = document.querySelector('div.rosetta-card');
            const btn = card?.querySelector('button[aria-label="Continue"]');
            if (!btn) return 'No continue button on card';
            
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
                return { error: err.message };
            }
        }''')
        print("Congrats Continue result:", res, flush=True)
        await asyncio.sleep(2.0)
        
        info = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            const btns = Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label')
            })).filter(b => b.text || b.aria);
            
            return {
                cardText: card ? card.innerText.slice(0, 300).replace(/\\n+/g, ' ') : 'No card',
                buttons: btns
            };
        }''')
        print("After click:", info['cardText'], flush=True)
        print("Buttons now:")
        for b in info['buttons']:
            if any(k in (b['text'] + str(b['aria'])).lower() for k in ['submit', 'finish', 'complete', 'continue', 'save']):
                print(" ->", b)

if __name__ == "__main__":
    asyncio.run(main())
