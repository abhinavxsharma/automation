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
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Continue');
            function getFiber(dom) {
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            
            let f = getFiber(btn);
            let results = [];
            let curr = f;
            while (curr && results.length < 25) {
                let typeName = typeof curr.type === 'string' ? curr.type : curr.type?.displayName || curr.type?.name || 'anonymous';
                let p = curr.memoizedProps || {};
                
                let summary = {
                    type: typeName,
                    propKeys: Object.keys(p)
                };
                
                if (p.onClick) {
                    summary.onClickStr = p.onClick.toString().slice(0, 300);
                }
                if (p.onContinue) {
                    summary.onContinueStr = p.onContinue.toString().slice(0, 300);
                }
                if (p.block) {
                    summary.block = {
                        id: p.block.id,
                        type: p.block.type,
                        isValid: p.block.isValid,
                        isComplete: p.block.isComplete,
                        data: p.block.data
                    };
                }
                
                results.push(summary);
                curr = curr.return;
            }
            return results;
        }''')
        print(json.dumps(info, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
