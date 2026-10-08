import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        res = await page.evaluate('''() => {
            const h3 = Array.from(document.querySelectorAll('h3, h2, h4')).find(el => el.textContent.includes('Model Failure Justification'));
            if (!h3) return { error: 'No Model Failure Justification heading' };
            const card = h3.closest('div[class*="rosetta-card"]');
            if (!card) return { error: 'No card' };
            
            const btn = Array.from(card.querySelectorAll('button')).find(b => b.textContent.trim() === 'Continue');
            if (!btn) return { error: 'No Continue button' };
            
            btn.click();
            return { success: true };
        }''')
        print("Click result:", res, flush=True)
        await asyncio.sleep(1.5)
        
        headings = await page.locator("h2, h3, h4").all_text_contents()
        print("Headings now:", [h.strip() for h in headings if h.strip()], flush=True)

if __name__ == "__main__":
    asyncio.run(main())
