import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        res = await page.evaluate('''() => {
            const exitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Exit');
            if (exitBtn) {
                exitBtn.click();
                return 'Clicked exit';
            }
            return 'Exit not found';
        }''')
        print("Exit click result:", res, flush=True)
        await asyncio.sleep(2.0)
        
        # Check current URL and any modal dialogs
        print("URL now:", page.url, flush=True)
        dialogs = await page.evaluate('''() => {
            const d = document.querySelector('div[role="dialog"], [class*="modal"]');
            return d ? d.innerText.slice(0, 300).replace(/\\n+/g, ' ') : 'No dialog';
        }''')
        print("Dialog text:", dialogs, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
