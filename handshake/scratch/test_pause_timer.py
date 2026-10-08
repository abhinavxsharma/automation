import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        btn = page.locator("button[aria-label='Pause timer']").first
        print("Pause timer visible:", await btn.is_visible(), flush=True)
        await btn.click()
        await asyncio.sleep(1.0)
        
        info = await page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label')
            })).filter(b => b.aria && (b.aria.includes('timer') || b.aria.includes('Resume') || b.aria.includes('Play')));
            return btns;
        }''')
        print("Timer buttons after click:", info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
