import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

JUSTIFICATION_TEXT = (
    "The model made a label-binding error between crossing edges in the diagram. "
    "It misassociated the numerical latency badges, assigning \\(21\\,\\text{ms}\\) "
    "(which belongs to directed edge \\(C\\to F\\)) to edge \\(D\\to E\\), which actually has a weight of \\(12\\,\\text{ms}\\).\n\n"
    "Because the earliest arrival time at node \\(D\\) is \\(L(D)=\\max(14+22,\\;18+15)=36\\,\\text{ms}\\), "
    "using \\(21\\,\\text{ms}\\) for \\(D\\to E\\) caused the model to compute "
    "\\(L(E)=\\max(23+17,\\;18+26,\\;36+21)=\\max(40,\\;44,\\;57)=57\\,\\text{ms}\\) "
    "instead of the correct value \\(L(E)=\\max(23+17,\\;18+26,\\;36+12)=\\max(40,\\;44,\\;48)=48\\,\\text{ms}\\). "
    "Propagating this inflated latency forward via \\(E\\to F\\) (\\(8\\,\\text{ms}\\)) and \\(F\\to T\\) (\\(20\\,\\text{ms}\\)), "
    "the model calculated \\(L(F)=57+8=65\\,\\text{ms}\\) and \\(L(T)=65+20=85\\,\\text{ms}\\), "
    "leading directly to its incorrect output of \\(85\\) instead of the ground truth critical path duration of \\(76\\,\\text{ms}\\)."
)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        # Locate the textarea inside Model Failure Justification card
        card = page.locator("div.rosetta-card:has-text('Model Failure Justification')")
        textarea = card.locator("textarea")
        
        print("Focusing textarea...", flush=True)
        await textarea.focus()
        await textarea.fill(JUSTIFICATION_TEXT)
        await asyncio.sleep(0.5)
        
        # Verify text filled
        val = await textarea.input_value()
        print(f"Textarea filled length: {len(val)}", flush=True)
        
        # Click Continue inside the card
        continue_btn = card.locator("button:has-text('Continue')")
        print("Clicking Continue...", flush=True)
        await continue_btn.click()
        await asyncio.sleep(1.5)
        
        headings = await page.locator("h2, h3, h4").all_text_contents()
        print("Headings after Step 15:", [h.strip() for h in headings if h.strip()], flush=True)

if __name__ == "__main__":
    asyncio.run(main())
