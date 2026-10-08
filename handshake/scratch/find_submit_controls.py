import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button, a')).map(b => {
                const rect = b.getBoundingClientRect();
                return {
                    tag: b.tagName,
                    text: b.innerText.trim(),
                    aria: b.getAttribute('aria-label'),
                    className: b.className,
                    disabled: b.disabled,
                    visible: rect.width > 0 && rect.height > 0,
                    x: Math.round(rect.x),
                    y: Math.round(rect.y),
                    w: Math.round(rect.width),
                    h: Math.round(rect.height)
                };
            }).filter(b => b.visible && (
                b.text.toLowerCase().includes('submit') ||
                b.text.toLowerCase().includes('save') ||
                b.text.toLowerCase().includes('finish') ||
                b.text.toLowerCase().includes('exit') ||
                b.text.toLowerCase().includes('continue') ||
                (b.aria && b.aria.toLowerCase().includes('submit')) ||
                (b.aria && b.aria.toLowerCase().includes('pause')) ||
                (b.aria && b.aria.toLowerCase().includes('timer'))
            ));
            
            return btns;
        }''')
        print(f"Found {len(info)} relevant buttons:")
        for b in info:
            print(f"[{b['tag']}] text='{b['text']}' aria='{b['aria']}' pos=({b['x']},{b['y']},{b['w']}x{b['h']}) disabled={b['disabled']}")

if __name__ == "__main__":
    asyncio.run(main())
