import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Continue');
            if (!btn) return { error: 'No continue button' };
            
            // Check button.form
            const form = btn.form;
            
            // Check event listeners / react fiber on button
            function getFiber(dom) {
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            
            let f = getFiber(btn);
            let handlers = [];
            let curr = f;
            while (curr) {
                if (curr.memoizedProps) {
                    const keys = Object.keys(curr.memoizedProps);
                    if (keys.some(k => k.toLowerCase().includes('click') || k.toLowerCase().includes('submit') || k.toLowerCase().includes('next'))) {
                        handlers.push({
                            type: curr.type?.name || typeof curr.type,
                            matchingProps: keys.filter(k => k.toLowerCase().includes('click') || k.toLowerCase().includes('submit') || k.toLowerCase().includes('next'))
                        });
                    }
                }
                curr = curr.return;
            }
            
            return {
                hasForm: !!form,
                formId: form ? form.id : null,
                formAction: form ? form.action : null,
                handlers: handlers.slice(0, 10)
            };
        }''')
        print("Continue Button Info:", info)

if __name__ == "__main__":
    asyncio.run(main())
