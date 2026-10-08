import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Save') || b.innerText.includes('Saved'));
            return {
                saveText: saveBtn ? saveBtn.innerText.trim() : 'No save button',
                saveDisabled: saveBtn ? saveBtn.disabled : null,
                url: window.location.href,
                title: document.title
            };
        }''')
        print("Save state:", info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
