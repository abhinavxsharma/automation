import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const sidebar = Array.from(document.querySelectorAll('div')).find(el => {
                const rect = el.getBoundingClientRect();
                return rect.left > window.innerWidth * 0.6 && rect.width > 250 && el.innerText.includes('items addressed');
            }) || Array.from(document.querySelectorAll('div')).find(el => {
                const rect = el.getBoundingClientRect();
                return rect.left > window.innerWidth * 0.6 && rect.width > 250 && el.innerText.includes('Feedback');
            });
            
            if (!sidebar) return { error: 'No sidebar found' };
            
            const btns = Array.from(sidebar.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                disabled: b.disabled
            }));
            
            return {
                text: sidebar.innerText,
                btns
            };
        }''')
        print("Sidebar Text:\n", info.get('text'))
        print("\nSidebar Buttons:\n", info.get('btns'))

if __name__ == "__main__":
    asyncio.run(main())
