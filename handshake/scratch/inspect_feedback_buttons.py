import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const items = Array.from(document.querySelectorAll('div, li')).filter(el => {
                return (el.innerText || '').includes('Jimson') && el.querySelectorAll('button').length > 0;
            });
            
            return items.map(it => {
                const text = it.innerText.slice(0, 100).replace(/\\n+/g, ' ');
                const btns = Array.from(it.querySelectorAll('button')).map(b => ({
                    text: b.innerText.trim(),
                    ariaLabel: b.getAttribute('aria-label'),
                    title: b.getAttribute('title'),
                    className: b.className,
                    outerHtml: b.outerHTML
                }));
                return { text, btns };
            });
        }''')
        for i, it in enumerate(info):
            print(f"[{i}] text: {it['text']}")
            for b in it['btns']:
                print(f"    button: text='{b['text']}' aria='{b['ariaLabel']}' title='{b['title']}'")

if __name__ == "__main__":
    asyncio.run(main())
