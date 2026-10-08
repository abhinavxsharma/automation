import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const b1 = document.querySelector('[data-block-id="039f2488-07d0-4a19-8725-d75aeb7625e4"]');
            const b2 = document.querySelector('[data-block-id="0021c8db-87c3-4c45-8eb6-27bbfafa7e94"]');
            return {
                block1: b1 ? b1.innerText : 'None',
                block2: b2 ? b2.innerText : 'None'
            };
        }''')
        print("=== BLOCK 1 (MODEL RESPONSE 1) ===")
        print(info['block1'])
        print("\n=== BLOCK 2 (MODEL RESPONSE 2) ===")
        print(info['block2'])

if __name__ == "__main__":
    asyncio.run(main())
