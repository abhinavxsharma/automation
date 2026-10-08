import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click the first Disagree button
        res = await page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button[aria-label="Disagree"]'));
            if (btns.length > 0) {
                btns[0].click();
                return 'Clicked first Disagree button';
            }
            return 'No Disagree buttons found';
        }''')
        print("Click result:", res, flush=True)
        await asyncio.sleep(1.0)
        
        # Check what changed in the DOM near that button
        info = await page.evaluate('''() => {
            const sidebar = Array.from(document.querySelectorAll('div')).find(el => {
                const rect = el.getBoundingClientRect();
                return rect.left > window.innerWidth * 0.6 && rect.width > 250 && el.innerText.includes('items addressed');
            });
            
            // Check for new inputs or textareas
            const inputs = Array.from(sidebar ? sidebar.querySelectorAll('input, textarea') : []).map(inp => ({
                tag: inp.tagName,
                type: inp.type,
                placeholder: inp.placeholder,
                value: inp.value
            }));
            
            const countText = sidebar?.innerText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/)?.[0];
            
            return {
                countText,
                inputs,
                sidebarSnippet: sidebar ? sidebar.innerText.slice(0, 400).replace(/\\n+/g, ' -- ') : ''
            };
        }''')
        print("After clicking Disagree:")
        print("Count:", info['countText'])
        print("Inputs:", info['inputs'])
        print("Snippet:", info['sidebarSnippet'])

if __name__ == "__main__":
    asyncio.run(main())
