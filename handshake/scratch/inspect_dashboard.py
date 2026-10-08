import asyncio
import sys
import json
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            // Find task card or row for 1520c7f4
            const allElements = Array.from(document.querySelectorAll('*'));
            const taskElements = allElements.filter(el => (el.innerText || '').includes('1520c'));
            
            // Get all buttons and links
            const actions = Array.from(document.querySelectorAll('button, a')).map(b => ({
                tag: b.tagName,
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                href: b.getAttribute('href'),
                className: b.className
            })).filter(b => b.text || b.aria);
            
            // Get headings / sections
            const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => h.innerText.trim()).filter(Boolean);
            
            // Get main text content
            const mainText = document.querySelector('main, #root, #__next')?.innerText?.slice(0, 2000)?.replace(/\\n+/g, ' ');
            
            return {
                headings,
                mainText,
                actions: actions.slice(0, 25)
            };
        }''')
        print("Headings:", info['headings'])
        print("\nMain text snippet:\n", info['mainText'][:500])
        print("\nActions:")
        for a in info['actions']:
            print(" -", a)

if __name__ == "__main__":
    asyncio.run(main())
