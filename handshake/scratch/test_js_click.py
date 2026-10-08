import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("Connecting...", flush=True)
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        print("Page connected:", page.url, flush=True)
        
        res = await page.evaluate('''() => {
            const radio = document.getElementById('radio-00289b96-5d4f-4efc-821c-14dd0cb7ae0a-0');
            if (!radio) return 'radio not found';
            
            // Dispatch click on radio
            radio.click();
            return {
                checked: radio.checked
            };
        }''')
        print("Radio clicked result:", res, flush=True)
        await asyncio.sleep(0.5)
        
        # Now let's see what the Continue button does
        cont_res = await page.evaluate('''async () => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Continue');
            if (!btn) return 'Continue not found';
            btn.click();
            return 'Continue clicked';
        }''')
        print("Continue result:", cont_res, flush=True)
        await asyncio.sleep(1.5)
        
        # Check headings
        headings = await page.locator("h2, h3, h4").all_text_contents()
        print("Headings after continue:", [h.strip() for h in headings if h.strip()], flush=True)

if __name__ == "__main__":
    asyncio.run(main())
