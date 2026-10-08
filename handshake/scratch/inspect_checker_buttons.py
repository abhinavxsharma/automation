import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const checkers = Array.from(document.querySelectorAll('*')).filter(el => {
                const t = el.innerText || '';
                return (t.includes('Prompt Checker') || t.includes('Model Failure Checker')) && el.querySelectorAll('button').length > 0;
            });
            
            return checkers.map(c => {
                const btns = Array.from(c.querySelectorAll('button')).map(b => ({
                    text: b.innerText.trim(),
                    aria: b.getAttribute('aria-label'),
                    title: b.getAttribute('title')
                }));
                return {
                    text: c.innerText.slice(0, 200).replace(/\\n+/g, ' '),
                    btns
                };
            });
        }''')
        print(f"Checkers with buttons: {len(info)}")
        for i, c in enumerate(info):
            print(f"[{i}] text: {c['text'][:100]}")
            print(f"    btns: {c['btns']}")

if __name__ == "__main__":
    asyncio.run(main())
