import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        raw_desc = await page.evaluate('''() => {
            const el = document.querySelector('[data-block-id="3993dc6e-cf3b-448e-873a-46d9bef303de"]');
            return el ? el.innerText : 'None';
        }''')
        print("=== IMAGE DESCRIPTION RAW ===")
        print(raw_desc)

if __name__ == "__main__":
    asyncio.run(main())
