import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click Next in sidebar
        res = await page.evaluate('''() => {
            const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
            if (nextBtn) {
                nextBtn.click();
                return 'Clicked Next';
            }
            return 'Next not found';
        }''')
        print("Click Next result:", res, flush=True)
        await asyncio.sleep(1.0)
        
        # Check current visible item or sidebar text
        sidebar_text = await page.evaluate('''() => {
            const sidebar = document.querySelector('[class*="sidebar"], [class*="feedback"]') || document.body;
            return sidebar.innerText.slice(0, 500).replace(/\\n+/g, ' -- ');
        }''')
        print("Sidebar after Next:\n", sidebar_text[:300])

if __name__ == "__main__":
    asyncio.run(main())
