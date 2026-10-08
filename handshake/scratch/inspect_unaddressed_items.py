import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const disagreeBtns = Array.from(document.querySelectorAll('button[aria-label="Disagree"]')).map(b => {
                const parent = b.closest('li, div[class*="item"], div[class*="card"], div') || b.parentElement;
                return {
                    text: parent ? parent.innerText.slice(0, 200).replace(/\\n+/g, ' ') : 'None',
                    disabled: b.disabled
                };
            });
            
            const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
            
            return {
                disagreeBtns,
                nextBtn: nextBtn ? {
                    text: nextBtn.innerText.trim(),
                    disabled: nextBtn.disabled,
                    outer: nextBtn.outerHTML
                } : null
            };
        }''')
        print(f"Disagree buttons ({len(info['disagreeBtns'])}):")
        for b in info['disagreeBtns']:
            print(" -", b['text'])
        print("\nNext button:", info['nextBtn'])

if __name__ == "__main__":
    asyncio.run(main())
