import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const h3 = Array.from(document.querySelectorAll('h3, h2, h4')).find(el => el.textContent.includes('Golden Solution'));
            if (!h3) return { error: 'No Golden Solution heading' };
            const card = h3.closest('div[class*="rosetta-card"]');
            if (!card) return { error: 'No card' };
            
            // Check all children, role="textbox", contenteditable, textarea, etc.
            const textboxes = Array.from(card.querySelectorAll('[contenteditable], [role="textbox"], textarea, input, div[class*="editor"], div[class*="ProseMirror"]')).map(el => ({
                tag: el.tagName,
                className: el.className,
                contentEditable: el.contentEditable,
                role: el.getAttribute('role'),
                text: el.innerText.slice(0, 200)
            }));
            
            return {
                cardHtml: card.innerHTML.slice(0, 2000),
                textboxes
            };
        }''')
        print("Textboxes:", info.get("textboxes"))
        print("\nCard HTML snippet:\n", info.get("cardHtml")[:1000])

if __name__ == "__main__":
    asyncio.run(main())
