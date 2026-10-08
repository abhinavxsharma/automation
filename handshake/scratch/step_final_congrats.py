import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click Continue on final congrats card
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
                return { error: err.message };
            }
        }''')
        print("Congrats Continue result:", res, flush=True)
        await asyncio.sleep(2.0)
        
        # Check overall page state, buttons, headings
        info = await page.evaluate('''() => {
            const cards = Array.from(document.querySelectorAll('div.rosetta-card'));
            const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                disabled: b.disabled
            })).filter(b => b.text || b.aria);
            
            const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => h.innerText.trim()).filter(Boolean);
            
            return {
                cardsCount: cards.length,
                headings: headings.slice(0, 15),
                buttons: buttons.slice(0, 20)
            };
        }''')
        print("Page state after congrats:", info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
