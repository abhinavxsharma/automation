import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        btn = page.locator("button[aria-label='View task without markdown or Latex formatting']").first
        print("Toggle button exists:", await btn.is_visible(), flush=True)
        await btn.click()
        await asyncio.sleep(1.0)
        
        # Check text of justification block now
        raw_text = await page.evaluate('''() => {
            const justBlock = document.querySelector('[data-block-id="eac54b4b-5677-48f0-bf86-228cfb012c57"]');
            return justBlock ? justBlock.innerText : 'None';
        }''')
        print("Text after toggle:\n", raw_text[:500], flush=True)
        
        # Toggle it back
        await btn.click()

if __name__ == "__main__":
    asyncio.run(main())
