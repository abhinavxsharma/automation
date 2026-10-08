import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        exit_btn = page.locator("button:has-text('Exit')").first
        print("Exit button visible:", await exit_btn.is_visible(), flush=True)
        await exit_btn.click()
        await asyncio.sleep(2.0)
        
        print("Current URL after Exit:", page.url, flush=True)
        print("Current Title:", await page.title(), flush=True)
        
        # Check buttons on the page
        btns = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('button, a')).map(b => ({
                tag: b.tagName,
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                href: b.getAttribute('href')
            })).filter(b => b.text || b.aria);
        }''')
        print(f"Buttons/Links found ({len(btns)}):")
        for b in btns[:15]:
            print(" -", b)

if __name__ == "__main__":
    asyncio.run(main())
