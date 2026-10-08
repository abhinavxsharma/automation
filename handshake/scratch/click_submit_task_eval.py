import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        res = await page.evaluate('''() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
            if (!btn) return 'Submit task button not found';
            btn.click();
            return 'Clicked Submit task';
        }''')
        print("Submit click result:", res, flush=True)
        await asyncio.sleep(2.0)
        
        # Check if dialog or modal appeared
        info = await page.evaluate('''() => {
            const dialog = document.querySelector('div[role="dialog"]');
            const btns = Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean);
            return {
                url: window.location.href,
                title: document.title,
                dialogText: dialog ? dialog.innerText.slice(0, 300).replace(/\\n+/g, ' ') : 'No dialog',
                buttons: btns
            };
        }''')
        print("After click info:", info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
