import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Navigate to task /run
        print("Navigating to task run...")
        await page.goto("https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run")
        await asyncio.sleep(4.0)
        
        # Check title and elements
        print("Title:", await page.title())
        
        # Check if start timer modal is up
        dialog = page.locator("button:has-text('Start timer')")
        if await dialog.is_visible():
            print("Clicking Start timer...")
            await dialog.click()
            await asyncio.sleep(2.0)
            
        # Check if the congrats card or any card is open
        card_text = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            return card ? card.innerText.slice(0, 300).replace(/\\n+/g, ' ') : 'No card';
        }''')
        print("Card text:", card_text)
        
        # Check all buttons
        btns = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                className: b.className
            })).filter(b => b.text || b.aria);
        }''')
        print(f"Buttons on page ({len(btns)}):")
        for b in btns:
            if any(k in (b['text'] + str(b['aria'])).lower() for k in ['save', 'submit', 'exit', 'continue', 'timer', 'feedback', 'edit']):
                print(" ->", b)

if __name__ == "__main__":
    asyncio.run(main())
