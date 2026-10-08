import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

REASONS = [
    "Replaced image with newly generated technical figure (dag_final_corrected.png). All node outlines are pure black (#000000). All latency badges are centered clearly on their unique directed edges with wide clearance away from crossings and competing lines (28 on D->T, 20 on F->T, 22 on A->D, 12 on D->E, 21 on C->F).",
    "Rewrote image description from scratch in neutral journal caption style (338 words). Confirmed black node outlines and removed all lists or mentions of crossing edges to eliminate solver hints.",
    "Converted all mathematical expressions, path formulas, dynamic programming evaluations, and latency values in both Golden Solution and Model Failure Justification to strict KaTeX formatting."
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Find the 3 textareas with placeholder 'Add a resolve reason'
        textareas = await page.locator("textarea[placeholder='Add a resolve reason']").all()
        print(f"Found {len(textareas)} resolve reason textareas", flush=True)
        
        for i, ta in enumerate(textareas):
            if i < len(REASONS):
                print(f"Filling reason {i+1}...", flush=True)
                await ta.focus()
                await ta.fill(REASONS[i])
                await asyncio.sleep(0.5)
        
        # Now find the Submit buttons next to each textarea
        # Let's inspect the Submit buttons in evaluate and click them
        res = await page.evaluate('''() => {
            const tas = Array.from(document.querySelectorAll('textarea[placeholder="Add a resolve reason"]'));
            let submitted = 0;
            for (let ta of tas) {
                // Find parent container or adjacent submit button
                const container = ta.closest('div[class*="comment"], div[class*="item"], form, li') || ta.parentElement?.parentElement;
                const submitBtn = container ? container.querySelector('button[aria-label="Submit"]') : null;
                if (submitBtn && !submitBtn.disabled) {
                    submitBtn.click();
                    submitted++;
                }
            }
            return { submitted };
        }''')
        print("Submitted resolve reasons:", res, flush=True)
        await asyncio.sleep(2.0)
        
        # Check remaining resolve reason textareas
        remaining = await page.locator("textarea[placeholder='Add a resolve reason']").count()
        print(f"Remaining resolve reason textareas: {remaining}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
