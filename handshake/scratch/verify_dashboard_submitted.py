import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click Go home
        print("Clicking 'Go home'...", flush=True)
        await page.evaluate('''() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Go home');
            if (btn) btn.click();
        }''')
        await asyncio.sleep(4.0)
        
        print("Dashboard URL:", page.url, flush=True)
        print("Dashboard Title:", await page.title(), flush=True)
        
        # Check task 1520c7f4 status on dashboard
        status = await page.evaluate('''() => {
            const taskCards = Array.from(document.querySelectorAll('*')).filter(el => {
                const t = el.innerText || '';
                return t.includes('1520c7f4') && el.innerText.length < 500 && el.innerText.length > 30;
            });
            return taskCards.map(c => c.innerText.replace(/\\n+/g, ' -- '));
        }''')
        print(f"Task cards for 1520c on dashboard ({len(status)}):")
        for s in status:
            print(" -", s)

if __name__ == "__main__":
    asyncio.run(main())
