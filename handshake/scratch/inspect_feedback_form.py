import asyncio
import sys
import json
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            // Find all inputs, textareas, and buttons in the right sidebar
            const sidebar = Array.from(document.querySelectorAll('div')).find(el => {
                const rect = el.getBoundingClientRect();
                return rect.left > window.innerWidth * 0.6 && rect.width > 250 && el.innerText.includes('Feedback');
            });
            
            if (!sidebar) return 'Sidebar not found';
            
            const inputs = Array.from(sidebar.querySelectorAll('input, textarea')).map(inp => ({
                tag: inp.tagName,
                type: inp.type,
                name: inp.name,
                id: inp.id,
                value: inp.value,
                placeholder: inp.placeholder,
                required: inp.required
            }));
            
            const buttons = Array.from(sidebar.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                disabled: b.disabled
            }));
            
            return {
                text: sidebar.innerText.slice(0, 1000),
                inputs,
                buttons
            };
        }''')
        print("Sidebar Text:\n", info.get('text'))
        print("\nSidebar Inputs:\n", info.get('inputs'))
        print("\nSidebar Buttons:\n", info.get('buttons'))

if __name__ == "__main__":
    asyncio.run(main())
