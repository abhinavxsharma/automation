import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        page = browser.contexts[0].pages[0]
        
        # Find scrollables and scroll down
        res = await page.evaluate('''() => {
            const scrollables = Array.from(document.querySelectorAll('*')).filter(e => {
                const s = window.getComputedStyle(e);
                return (s.overflowY === 'auto' || s.overflowY === 'scroll') && e.scrollHeight > e.clientHeight;
            });
            let scrolled = [];
            for (const s of scrollables) {
                s.scrollTop += 1200;
                scrolled.push({tag: s.tagName, className: s.className, scrollHeight: s.scrollHeight, scrollTop: s.scrollTop});
            }
            return scrolled;
        }''')
        print("Scrolled containers:", res)
        await asyncio.sleep(1)
        await page.screenshot(path='handshake/scratch/scroll_div.png')
        print('Saved scroll_div.png')

if __name__ == '__main__':
    asyncio.run(main())
