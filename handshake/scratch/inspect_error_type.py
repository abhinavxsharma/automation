import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Look for the Error Type container
        res = await page.evaluate('''() => {
            const h3 = Array.from(document.querySelectorAll('h3, h2, h4')).find(el => el.textContent.includes('Error Type'));
            if (!h3) return 'Error Type heading not found';
            const card = h3.closest('div[class*="card"], div[class*="step"], form, div[style*="border"], div[class*="container"]') || h3.parentElement;
            
            const radios = Array.from(card.querySelectorAll('input[type="radio"]')).map(r => ({
                id: r.id,
                name: r.name,
                value: r.value,
                checked: r.checked,
                label: r.closest('label')?.textContent?.trim() || r.parentElement?.textContent?.trim()
            }));
            
            return {
                cardHtml: card.outerHTML.slice(0, 1000),
                radios
            };
        }''')
        print("Inspection:", res)

if __name__ == "__main__":
    asyncio.run(main())
