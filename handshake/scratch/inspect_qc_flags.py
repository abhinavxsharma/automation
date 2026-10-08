import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        flags = await page.evaluate('''() => {
            const checkers = Array.from(document.querySelectorAll('*')).filter(el => {
                const t = el.innerText || '';
                return t.includes('Prompt Checker') || t.includes('Model Failure Checker');
            });
            
            // Get unique containers
            const results = [];
            document.querySelectorAll('div').forEach(el => {
                if (el.innerText && (el.innerText.includes('Prompt Checker - Lumiere') || el.innerText.includes('Model Failure Checker - Lumiere'))) {
                    if (el.innerText.length < 1000 && !results.some(r => r.includes(el.innerText.slice(0, 100)))) {
                        results.push(el.innerText);
                    }
                }
            });
            return results;
        }''')
        print(f"Found {len(flags)} checker texts:")
        for i, f in enumerate(flags):
            print(f"--- Checker {i} ---")
            print(f)

if __name__ == "__main__":
    asyncio.run(main())
