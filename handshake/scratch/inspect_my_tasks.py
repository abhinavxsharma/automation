import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            // Find task items in "My tasks"
            const cards = Array.from(document.querySelectorAll('div, tr, li')).filter(el => {
                const t = el.innerText || '';
                return t.includes('1520c') || t.includes('task-dependency directed acyclic graph');
            });
            
            // Get unique closest containers
            const unique = [];
            for (let c of cards) {
                if (c.innerText.length < 500 && !unique.some(u => u.text.includes(c.innerText.slice(0, 50)))) {
                    const btns = Array.from(c.querySelectorAll('button, a')).map(b => ({
                        tag: b.tagName,
                        text: b.innerText.trim(),
                        aria: b.getAttribute('aria-label'),
                        href: b.getAttribute('href')
                    }));
                    unique.push({
                        text: c.innerText.replace(/\\n+/g, ' -- '),
                        btns
                    });
                }
            }
            return unique;
        }''')
        print(f"Found {len(info)} task elements:")
        for it in info:
            print("---")
            print(it['text'])
            print("Actions:", it['btns'])

if __name__ == "__main__":
    asyncio.run(main())
