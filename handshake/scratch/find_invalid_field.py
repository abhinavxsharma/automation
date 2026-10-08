import asyncio
import sys
import json
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        errors = await page.evaluate('''() => {
            function getFiber(dom) {
                if (!dom) return null;
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
            let f = getFiber(btn);
            
            // Check Save button onClick source
            let onClick = f?.memoizedProps?.onClick;
            let onClickSource = onClick ? onClick.toString().slice(0, 500) : 'None';
            
            // Find all blocks and check their values or validation status
            const blocks = Array.from(document.querySelectorAll('[data-block-id]')).map(el => {
                const blockId = el.getAttribute('data-block-id');
                const bf = getFiber(el);
                let blockData = null;
                let curr = bf;
                while (curr) {
                    if (curr.memoizedProps?.block) {
                        blockData = {
                            id: curr.memoizedProps.block.id,
                            type: curr.memoizedProps.block.type,
                            isValid: curr.memoizedProps.block.isValid,
                            isComplete: curr.memoizedProps.block.isComplete
                        };
                        break;
                    }
                    curr = curr.return;
                }
                return {
                    blockId,
                    blockData,
                    text: el.innerText.slice(0, 100).replace(/\\n+/g, ' ')
                };
            });
            
            return {
                onClickSource,
                blocks
            };
        }''')
        print("Save button onClick:", errors['onClickSource'])
        print(f"\nBlocks ({len(errors['blocks'])}):")
        for b in errors['blocks']:
            print(f"- {b['blockId']} | data: {b['blockData']} | text: {b['text'][:60]}")

if __name__ == "__main__":
    asyncio.run(main())
