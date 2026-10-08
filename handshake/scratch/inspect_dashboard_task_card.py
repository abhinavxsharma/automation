import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Navigate to dashboard
        await page.goto("https://ai.joinhandshake.com/fellow/15f2e875-62ac-492c-9e96-d5569635671a/tasks")
        await asyncio.sleep(3.0)
        
        info = await page.evaluate('''() => {
            const taskRow = Array.from(document.querySelectorAll('*')).find(el => {
                return (el.innerText || '').includes('1520c') && el.innerText.length < 600 && el.innerText.length > 50;
            });
            
            if (!taskRow) return 'Task row not found';
            
            const btns = Array.from(taskRow.querySelectorAll('button, a')).map(b => ({
                tag: b.tagName,
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                className: b.className,
                outer: b.outerHTML
            }));
            
            return {
                html: taskRow.innerHTML,
                text: taskRow.innerText,
                btns
            };
        }''')
        print("Task row text:\n", info.get('text'))
        print("\nTask row buttons:")
        for b in info.get('btns', []):
            print(" -", b['tag'], b['text'], b['aria'])

if __name__ == "__main__":
    asyncio.run(main())
