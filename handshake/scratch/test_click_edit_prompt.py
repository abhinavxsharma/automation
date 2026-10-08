import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click Edit this step on Block 9
        res = await page.evaluate('''() => {
            const promptBlock = document.querySelector('[data-block-id="9e254568-dd1a-476f-9eb5-d49807d95930"]');
            const editBtn = promptBlock ? promptBlock.querySelector('button[aria-label="Edit this step"]') : null;
            if (editBtn) {
                editBtn.click();
                return 'Clicked edit button';
            }
            return 'Edit button not found';
        }''')
        print("Click edit result:", res, flush=True)
        await asyncio.sleep(2.0)
        
        # Check active card or modal
        card_info = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            const dialog = document.querySelector('div[role="dialog"]');
            return {
                cardText: card ? card.innerText.slice(0, 300).replace(/\\n+/g, ' ') : 'No card',
                dialogText: dialog ? dialog.innerText.slice(0, 300).replace(/\\n+/g, ' ') : 'No dialog'
            };
        }''')
        print("State after edit click:", card_info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
