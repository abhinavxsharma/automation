import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const promptBlock = document.querySelector('[data-block-id="9e254568-dd1a-476f-9eb5-d49807d95930"]');
            const editBtn = promptBlock ? promptBlock.querySelector('button[aria-label="Edit this step"]') : null;
            
            return {
                blockFound: !!promptBlock,
                editBtnFound: !!editBtn,
                promptText: promptBlock ? promptBlock.innerText.slice(0, 300) : null
            };
        }''')
        print("Edit prompt info:", info)

if __name__ == "__main__":
    asyncio.run(main())
