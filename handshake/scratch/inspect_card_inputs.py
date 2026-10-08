import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const h3 = Array.from(document.querySelectorAll('h3, h2, h4')).find(el => el.textContent.includes('Error Type'));
            if (!h3) return { error: 'No Error Type heading' };
            const card = h3.closest('div[class*="rosetta-card"]');
            if (!card) return { error: 'No card' };
            
            const inputs = Array.from(card.querySelectorAll('input, textarea, select')).map(el => ({
                tag: el.tagName,
                type: el.type,
                name: el.name,
                id: el.id,
                value: el.value,
                placeholder: el.placeholder,
                required: el.required
            }));
            
            const buttons = Array.from(card.querySelectorAll('button')).map(b => ({
                text: b.textContent.trim(),
                disabled: b.disabled,
                type: b.type
            }));
            
            const fullText = card.innerText;
            
            return { inputs, buttons, fullText };
        }''')
        print("Card Info:")
        print("Full Text:\n", info.get("fullText"))
        print("\nInputs:\n", info.get("inputs"))
        print("\nButtons:\n", info.get("buttons"))

if __name__ == "__main__":
    asyncio.run(main())
