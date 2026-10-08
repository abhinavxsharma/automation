import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        page = browser.contexts[0].pages[0]
        
        for i in range(20):
            print(f"--- Check {i+1} ---")
            # Check for spinners or text
            spinners = await page.locator('svg.animate-spin, [aria-label*="loading" i], [aria-label*="generating" i]').count()
            # Check visible buttons
            buttons = []
            for b in await page.locator('button').all():
                if await b.is_visible():
                    t = (await b.inner_text()).strip()
                    a = await b.get_attribute('aria-label') or ''
                    if t or a:
                        buttons.append(f"{t or a}")
                        
            print(f"Buttons count: {len(buttons)}, Spinners: {spinners}")
            # Take screenshot every 5 checks
            if i % 3 == 0:
                await page.screenshot(path=f'handshake/scratch/regen_check_{i}.png')
                print(f"Saved regen_check_{i}.png")
                
            # Check if model response blocks are visible
            body_text = await page.evaluate("() => document.body ? document.body.innerText : ''")
            has_b1 = "Model Response 1" in body_text or "Model response 1" in body_text or "model responses" in body_text.lower()
            has_b2 = "Model Response 2" in body_text or "Model response 2" in body_text or "block 2" in body_text.lower()
            print(f"has_b1: {has_b1}, has_b2: {has_b2}")
            
            await asyncio.sleep(4)

if __name__ == '__main__':
    asyncio.run(main())
