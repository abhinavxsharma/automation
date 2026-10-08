import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const h3 = Array.from(document.querySelectorAll('h3, h2, h4')).find(el => el.textContent.includes('Model Failure Justification'));
            if (!h3) return { error: 'No Model Failure Justification heading' };
            const card = h3.closest('div[class*="rosetta-card"]');
            if (!card) return { error: 'No card' };
            
            const inputs = Array.from(card.querySelectorAll('input, textarea, div[contenteditable="true"]')).map(el => ({
                tag: el.tagName,
                type: el.type,
                name: el.name,
                id: el.id,
                value: el.value || el.innerText,
                className: el.className
            }));
            
            const buttons = Array.from(card.querySelectorAll('button')).map(b => ({
                text: b.textContent.trim(),
                disabled: b.disabled
            }));
            
            return {
                heading: h3.textContent.trim(),
                cardText: card.innerText.slice(0, 500),
                inputs,
                buttons
            };
        }''')
        print("Step 15 Info:", info)

if __name__ == "__main__":
    asyncio.run(main())
