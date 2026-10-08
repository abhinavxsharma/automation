import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const dialog = document.querySelector('div[role="dialog"]');
            if (!dialog) return 'No dialog found';
            
            const btns = Array.from(dialog.querySelectorAll('button, a')).map(b => ({
                tag: b.tagName,
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                className: b.className
            }));
            
            return {
                text: dialog.innerText,
                btns
            };
        }''')
        print("Modal info:", info)

if __name__ == "__main__":
    asyncio.run(main())
