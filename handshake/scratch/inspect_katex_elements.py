import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const justBlock = document.querySelector('[data-block-id="eac54b4b-5677-48f0-bf86-228cfb012c57"]');
            const katexEls = justBlock ? justBlock.querySelectorAll('.katex, [class*="katex"], [class*="math"]') : [];
            const paragraphs = justBlock ? Array.from(justBlock.querySelectorAll('p')).map(p => p.innerHTML) : [];
            
            return {
                katexCount: katexEls.length,
                paragraphs
            };
        }''')
        print("Katex count:", info['katexCount'])
        print("Paragraphs in Justification:")
        for p in info['paragraphs']:
            print("---")
            print(p)

if __name__ == "__main__":
    asyncio.run(main())
