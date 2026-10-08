import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Click Save
        res = await page.evaluate('''async () => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
            if (!btn) return 'Save button not found';
            
            function getFiber(dom) {
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            let f = getFiber(btn);
            let onClick = f?.memoizedProps?.onClick;
            if (onClick) {
                let ret = await onClick();
                return { success: true, ret: String(ret) };
            } else {
                btn.click();
                return { success: true, method: 'dom click' };
            }
        }''')
        print("Save result:", res, flush=True)
        await asyncio.sleep(2.0)
        
        # Check toast or status
        status = await page.evaluate('''() => {
            const toast = document.querySelector('[role="status"], [role="alert"], .toast, div[class*="toast"]');
            return toast ? toast.innerText : 'No toast';
        }''')
        print("Toast after save:", status, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
