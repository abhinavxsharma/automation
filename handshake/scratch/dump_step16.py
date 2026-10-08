import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        page = browser.contexts[0].pages[0]
        html = await page.evaluate('''() => {
            const h3 = Array.from(document.querySelectorAll('h3, h2, h4')).find(el => el.textContent.includes('Golden Solution'));
            const card = h3 ? h3.closest('div[class*="rosetta-card"]') : null;
            return card ? card.innerHTML : 'No card';
        }''')
        with open('scratch/step16_card.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print('Written length:', len(html))

if __name__ == '__main__':
    asyncio.run(main())
