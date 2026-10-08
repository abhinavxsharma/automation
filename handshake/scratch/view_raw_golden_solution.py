import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Check text of Golden Solution block in raw view
        raw_text = await page.evaluate('''() => {
            const gsBlock = document.querySelector('[data-block-id="831895bf-4f9f-4e8f-9d56-8f6a8d80443f"]');
            return gsBlock ? gsBlock.innerText : 'None';
        }''')
        
        print("=== GOLDEN SOLUTION RAW TEXT ===")
        print("Length:", len(raw_text))
        print("First 500 chars:\n", raw_text[:500])
        print("\nStep 5 snippet:\n")
        idx = raw_text.find("Step 5")
        if idx != -1:
            print(raw_text[idx:idx+1500])
        else:
            print("Step 5 not found!")

if __name__ == "__main__":
    asyncio.run(main())
