import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button, a')).map(b => ({
                tag: b.tagName,
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                href: b.getAttribute('href'),
                disabled: b.disabled
            })).filter(b => b.text || b.aria || b.href);
            
            // Check top header specifically
            const header = document.querySelector('nav, header, div[class*="header"], div[class*="nav"]') || document.body;
            
            return {
                url: window.location.href,
                headerButtons: btns.filter(b => ['Save', 'Exit', 'Submit', 'Continue', 'Pause timer'].some(k => (b.text + b.aria).includes(k)))
            };
        }''')
        print("URL:", info['url'])
        print("Header controls:")
        for b in info['headerButtons']:
            print(" -", b)

if __name__ == "__main__":
    asyncio.run(main())
