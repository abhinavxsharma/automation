import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        res = await page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button[aria-label="Resolve"]'));
            let results = [];
            for (let b of btns) {
                // Find card or text
                let p = b.parentElement;
                while (p && !p.innerText.includes('Jimson')) {
                    p = p.parentElement;
                }
                results.push({
                    text: p ? p.innerText.slice(0, 100).replace(/\\n+/g, ' ') : 'unknown',
                    disabled: b.disabled
                });
            }
            return results;
        }''')
        print(f"Resolve buttons count: {len(res)}")
        for r in res:
            print(" -", r)

if __name__ == "__main__":
    asyncio.run(main())
