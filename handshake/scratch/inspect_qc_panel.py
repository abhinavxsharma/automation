import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            // Find sidebar / feedback / QC panels
            const panels = Array.from(document.querySelectorAll('[class*="feedback"], [class*="qc"], [class*="sidebar"], [data-testid*="feedback"], [data-testid*="qc"]'));
            
            // Look for text in the right pane or any element containing 'Checker' or 'Judge' or 'Feedback'
            const allElements = Array.from(document.querySelectorAll('*')).filter(el => {
                const text = el.innerText || '';
                return text.includes('Prompt Checker') || text.includes('Model Failure Checker') || text.includes('Science Judge') || text.includes('Feedback');
            });
            
            // Check right side of page
            const rightPane = Array.from(document.querySelectorAll('div')).filter(el => {
                const rect = el.getBoundingClientRect();
                return rect.left > window.innerWidth * 0.6 && rect.width > 200 && el.innerText.length > 50;
            }).map(el => ({
                tag: el.tagName,
                className: el.className,
                text: el.innerText.slice(0, 1000)
            }));
            
            return {
                rightPane: rightPane.slice(0, 3)
            };
        }''')
        for i, pane in enumerate(info.get('rightPane', [])):
            print(f"=== Pane {i} ===")
            print(pane['text'][:500])

if __name__ == "__main__":
    asyncio.run(main())
