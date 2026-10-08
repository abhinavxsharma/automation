import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const modal = document.querySelector('div[role="dialog"]');
            if (!modal) return 'No modal';
            
            const btns = Array.from(modal.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label')
            }));
            
            return {
                text: modal.innerText.replace(/\\n+/g, ' '),
                btns
            };
        }''')
        print("Exit modal info:", info)

if __name__ == "__main__":
    asyncio.run(main())
