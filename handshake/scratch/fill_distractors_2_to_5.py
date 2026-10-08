import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

DISTRACTORS = [
    ("Distractor #2", "89"),
    ("Distractor #3", "72"),
    ("Distractor #4", "68"),
    ("Distractor #5", "64")
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        for name, val in DISTRACTORS:
            print(f"Processing {name} -> {val}...", flush=True)
            
            # Check current card text
            curr_text = await page.evaluate('''() => {
                const card = document.querySelector('div.rosetta-card');
                return card ? card.innerText.slice(0, 100).replace(/\\n+/g, ' ') : null;
            }''')
            print(f"  Current card: {curr_text}", flush=True)
            
            # Fill textarea
            card = page.locator("div.rosetta-card")
            textarea = card.locator("textarea")
            await textarea.focus()
            await textarea.fill(val)
            await asyncio.sleep(0.3)
            
            # Call Continue onClick
            res = await page.evaluate('''async () => {
                const btn = document.querySelector("div.rosetta-card button[aria-label='Continue']");
                if (!btn) return 'No button';
                function getFiber(dom) {
                    const key = Object.keys(dom).find(k => k.startsWith('__reactFiber$'));
                    return key ? dom[key] : null;
                }
                let f = getFiber(btn);
                let onClick = f?.memoizedProps?.onClick;
                if (!onClick) return 'No onClick prop';
                try {
                    let ret = await onClick();
                    return { success: true, ret: String(ret) };
                } catch (err) {
                    return { error: err.message };
                }
            }''')
            print(f"  Continue result: {res}", flush=True)
            await asyncio.sleep(1.5)
            
        # Check what card appears after Distractor 5
        final_info = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            return {
                text: card ? card.innerText.slice(0, 300).replace(/\\n+/g, ' ') : 'No card',
                heading: card?.querySelector('h1, h2, h3, h4, h5, h6')?.innerText?.trim(),
                buttons: Array.from(card?.querySelectorAll('button') || []).map(b => b.innerText.trim()).filter(Boolean)
            };
        }''')
        print("\nCard after all distractors:", final_info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
