import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Confirm time');
            const parent = btn ? btn.closest('div[class*="modal"], div[class*="dialog"], div[class*="card"], div') : null;
            
            // Get all text in the confirm container
            return {
                btnFound: !!btn,
                containerText: parent ? parent.innerText : 'None'
            };
        }''')
        print("Confirm time info:\n", info)

if __name__ == "__main__":
    asyncio.run(main())
