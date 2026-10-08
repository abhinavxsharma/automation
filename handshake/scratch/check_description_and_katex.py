import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const descBlock = document.querySelector('[data-block-id="3993dc6e-cf3b-448e-873a-46d9bef303de"]');
            const justBlock = document.querySelector('[data-block-id="eac54b4b-5677-48f0-bf86-228cfb012c57"]');
            const gsBlock = document.querySelector('[data-block-id="831895bf-4f9f-4e8f-9d56-8f6a8d80443f"]');
            
            return {
                descText: descBlock ? descBlock.innerText : '',
                justText: justBlock ? justBlock.innerText : '',
                gsText: gsBlock ? gsBlock.innerText : ''
            };
        }''')
        
        print("=== IMAGE DESCRIPTION TEXT ===")
        print(info['descText'])
        
        print("\n=== MODEL FAILURE JUSTIFICATION TEXT ===")
        print(info['justText'][:500])
        
        print("\n=== GOLDEN SOLUTION TEXT (SAMPLE) ===")
        print(info['gsText'][:500])

if __name__ == "__main__":
    asyncio.run(main())
