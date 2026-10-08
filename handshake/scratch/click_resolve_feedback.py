import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        res = await page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button[aria-label="Resolve"]'));
            let clicked = 0;
            for (let b of btns) {
                b.click();
                clicked++;
            }
            return { clicked };
        }''')
        print(f"Clicked resolve on {res['clicked']} buttons", flush=True)
        await asyncio.sleep(1.0)
        
        # Check remaining resolve buttons
        remaining = await page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button[aria-label="Resolve"]'));
            return btns.length;
        }''')
        print("Remaining resolve buttons:", remaining, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
