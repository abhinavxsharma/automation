import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const h3 = Array.from(document.querySelectorAll('h3, h2, h4')).find(el => el.textContent.includes('Error Type'));
            if (!h3) return 'No Error Type heading';
            const card = h3.closest('div[class*="rosetta-card"]');
            if (!card) return 'No card';
            
            const inputs = Array.from(card.querySelectorAll('input[type="radio"]'));
            return inputs.map(inp => {
                let parent = inp.parentElement;
                let text = inp.closest('label')?.innerText || parent?.innerText;
                let rect = inp.getBoundingClientRect();
                return {
                    id: inp.id,
                    value: inp.value,
                    checked: inp.checked,
                    outerHtml: inp.outerHTML,
                    parentHtml: parent ? parent.outerHTML.slice(0, 200) : null,
                    text: text,
                    x: rect.x,
                    y: rect.y,
                    w: rect.width,
                    h: rect.height
                };
            });
        }''')
        print("Radios info:", info)

if __name__ == "__main__":
    asyncio.run(main())
