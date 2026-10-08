import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
            function getFiber(dom) {
                if (!dom) return null;
                const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                return key ? dom[key] : null;
            }
            
            let f = getFiber(btn);
            let curr = f;
            let results = [];
            while (curr && results.length < 20) {
                let typeName = typeof curr.type === 'string' ? curr.type : curr.type?.displayName || curr.type?.name || 'anonymous';
                let props = curr.memoizedProps ? Object.keys(curr.memoizedProps) : [];
                
                // Check if any props or state has onSave, save, etc.
                let saveProp = null;
                if (curr.memoizedProps) {
                    for (let k of Object.keys(curr.memoizedProps)) {
                        if (k.toLowerCase().includes('save')) {
                            saveProp = { [k]: curr.memoizedProps[k]?.toString().slice(0, 300) };
                        }
                    }
                }
                
                results.push({
                    type: typeName,
                    props: props.slice(0, 10),
                    saveProp
                });
                curr = curr.return;
            }
            return results;
        }''')
        for r in info:
            print(f"- {r['type']} | save: {r['saveProp']}")

if __name__ == "__main__":
    asyncio.run(main())
