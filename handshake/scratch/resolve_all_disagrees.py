import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

REASONS = [
    "The DAG graph, task dependencies, and edge latency weights are fully specified via the uploaded multimodal technical figure (dag_final_corrected.png). No external reference is needed.",
    "The prompt asks to determine the critical-path duration of the parallel computation pipeline DAG, which uniquely specifies computing the maximum-latency path from source S to sink T via dynamic programming.",
    "The model in Block 1 failed on the diagram by confusing crossing edge labels (assigning 21 ms from C->F to D->E), producing an incorrect output of 85 ms instead of the ground truth critical path duration of 76 ms."
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # 1. Fill the currently open 'Reason for disagreeing' textarea (Prompt Checker)
        ta1 = page.locator("textarea[placeholder='Reason for disagreeing']").first
        if await ta1.is_visible():
            print("Filling reason 1...", flush=True)
            await ta1.focus()
            await ta1.fill(REASONS[0])
            await asyncio.sleep(0.5)
            
            # Submit it
            res1 = await page.evaluate('''() => {
                const ta = document.querySelector('textarea[placeholder="Reason for disagreeing"]');
                const container = ta?.closest('div[class*="item"], div[class*="card"], li, form') || ta?.parentElement?.parentElement;
                const btn = container ? container.querySelector('button[aria-label="Submit"]') : null;
                if (btn && !btn.disabled) {
                    btn.click();
                    return 'Submitted reason 1';
                }
                return 'Submit 1 not clickable';
            }''')
            print("Submit 1:", res1, flush=True)
            await asyncio.sleep(1.5)
            
        # 2. Click Disagree on the second item (Science Judge)
        print("Clicking Disagree on item 2...", flush=True)
        await page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button[aria-label="Disagree"]'));
            if (btns.length > 0) btns[0].click();
        }''')
        await asyncio.sleep(1.0)
        
        ta2 = page.locator("textarea[placeholder='Reason for disagreeing']").first
        if await ta2.is_visible():
            print("Filling reason 2...", flush=True)
            await ta2.focus()
            await ta2.fill(REASONS[1])
            await asyncio.sleep(0.5)
            
            res2 = await page.evaluate('''() => {
                const ta = document.querySelector('textarea[placeholder="Reason for disagreeing"]');
                const container = ta?.closest('div[class*="item"], div[class*="card"], li, form') || ta?.parentElement?.parentElement;
                const btn = container ? container.querySelector('button[aria-label="Submit"]') : null;
                if (btn && !btn.disabled) {
                    btn.click();
                    return 'Submitted reason 2';
                }
                return 'Submit 2 not clickable';
            }''')
            print("Submit 2:", res2, flush=True)
            await asyncio.sleep(1.5)

        # 3. Click Disagree on the third item (Model Failure Checker)
        print("Clicking Disagree on item 3...", flush=True)
        await page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button[aria-label="Disagree"]'));
            if (btns.length > 0) btns[0].click();
        }''')
        await asyncio.sleep(1.0)
        
        ta3 = page.locator("textarea[placeholder='Reason for disagreeing']").first
        if await ta3.is_visible():
            print("Filling reason 3...", flush=True)
            await ta3.focus()
            await ta3.fill(REASONS[2])
            await asyncio.sleep(0.5)
            
            res3 = await page.evaluate('''() => {
                const ta = document.querySelector('textarea[placeholder="Reason for disagreeing"]');
                const container = ta?.closest('div[class*="item"], div[class*="card"], li, form') || ta?.parentElement?.parentElement;
                const btn = container ? container.querySelector('button[aria-label="Submit"]') : null;
                if (btn && !btn.disabled) {
                    btn.click();
                    return 'Submitted reason 3';
                }
                return 'Submit 3 not clickable';
            }''')
            print("Submit 3:", res3, flush=True)
            await asyncio.sleep(1.5)

        # Check final count text in sidebar!
        final_info = await page.evaluate('''() => {
            const sidebar = Array.from(document.querySelectorAll('div')).find(el => {
                const rect = el.getBoundingClientRect();
                return rect.left > window.innerWidth * 0.6 && rect.width > 250 && el.innerText.includes('items addressed');
            }) || Array.from(document.querySelectorAll('div')).find(el => {
                const rect = el.getBoundingClientRect();
                return rect.left > window.innerWidth * 0.6 && rect.width > 250 && el.innerText.includes('Feedback');
            });
            
            return {
                text: sidebar ? sidebar.innerText.slice(0, 500).replace(/\\n+/g, ' -- ') : 'No sidebar'
            };
        }''')
        print("\nFinal Sidebar State:\n", final_info['text'])

if __name__ == "__main__":
    asyncio.run(main())
