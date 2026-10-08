import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        page = browser.contexts[0].pages[0]
        
        # Check textareas
        tas = await page.locator('textarea').all()
        print(f"Total textareas: {len(tas)}")
        for i, ta in enumerate(tas):
            print(f"Textarea {i} visible: {await ta.is_visible()}")
            
        # Check file inputs
        file_inputs = await page.locator('input[type="file"]').all()
        print(f"Total file inputs: {len(file_inputs)}")
        
        # Check buttons in the active editor
        # Let's inspect buttons inside the card
        buttons = await page.locator('button').all()
        for i, b in enumerate(buttons):
            if await b.is_visible():
                text = (await b.inner_text()).strip()
                aria = await b.get_attribute('aria-label') or ''
                if text or aria:
                    print(f"Button {i}: text='{text}', aria='{aria}'")

if __name__ == '__main__':
    asyncio.run(main())
