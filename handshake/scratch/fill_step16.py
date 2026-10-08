import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

GOLDEN_SOLUTION_TEXT = """Step 1: Extract the DAG topology and edge latencies from the diagram.
The vertices are \(S, A, B, C, D, E, F, T\), with source \(S\) and sink \(T\). The directed edges and their respective latency weights (in milliseconds) are:
- \(S\\to A = 14\\,\\text{ms}\)
- \(S\\to B = 18\\,\\text{ms}\)
- \(S\\to C = 11\\,\\text{ms}\)
- \(A\\to C = 9\\,\\text{ms}\)
- \(A\\to D = 22\\,\\text{ms}\)
- \(B\\to D = 15\\,\\text{ms}\)
- \(B\\to E = 26\\,\\text{ms}\)
- \(C\\to E = 17\\,\\text{ms}\)
- \(C\\to F = 21\\,\\text{ms}\)
- \(D\\to E = 12\\,\\text{ms}\)
- \(D\\to F = 19\\,\\text{ms}\)
- \(D\\to T = 28\\,\\text{ms}\)
- \(E\\to F = 8\\,\\text{ms}\)
- \(E\\to T = 24\\,\\text{ms}\)
- \(F\\to T = 20\\,\\text{ms}\)

Step 2: Establish a topological ordering of the vertices.
A valid topological ordering respecting all directed dependencies is:
\(S, A, B, C, D, E, F, T\).
We define \(L(u)\) as the longest-path duration (maximum latency) from the source vertex \(S\) to vertex \(u\). For the source node, \(L(S) = 0\\,\\text{ms}\).

Step 3: Compute the maximum latencies to intermediate nodes \(A\), \(B\), \(C\), and \(D\) using dynamic programming.
- For node \(A\), the only incoming edge is from \(S\):
  \(L(A) = L(S) + 14 = 0 + 14 = 14\\,\\text{ms}\)
- For node \(B\), the only incoming edge is from \(S\):
  \(L(B) = L(S) + 18 = 0 + 18 = 18\\,\\text{ms}\)
- For node \(C\), incoming edges arrive from \(S\) and \(A\):
  \(L(C) = \\max(L(S) + 11,\\; L(A) + 9) = \\max(11,\\; 14 + 9) = \\max(11,\\; 23) = 23\\,\\text{ms}\)
- For node \(D\), incoming edges arrive from \(A\) and \(B\):
  \(L(D) = \\max(L(A) + 22,\\; L(B) + 15) = \\max(14 + 22,\\; 18 + 15) = \\max(36,\\; 33) = 36\\,\\text{ms}\)

Step 4: Compute the maximum latencies to nodes \(E\), \(F\), and sink \(T\).
- For node \(E\), incoming edges arrive from \(C\), \(B\), and \(D\):
  \(L(E) = \\max(L(C) + 17,\\; L(B) + 26,\\; L(D) + 12) = \\max(23 + 17,\\; 18 + 26,\\; 36 + 12) = \\max(40,\\; 44,\\; 48) = 48\\,\\text{ms}\)
- For node \(F\), incoming edges arrive from \(C\), \(D\), and \(E\):
  \(L(F) = \\max(L(C) + 21,\\; L(D) + 19,\\; L(E) + 8) = \\max(23 + 21,\\; 36 + 19,\\; 48 + 8) = \\max(44,\\; 55,\\; 56) = 56\\,\\text{ms}\)
- For sink node \(T\), incoming edges arrive from \(D\), \(E\), and \(F\):
  \(L(T) = \\max(L(D) + 28,\\; L(E) + 24,\\; L(F) + 20) = \\max(36 + 28,\\; 48 + 24,\\; 56 + 20) = \\max(64,\\; 72,\\; 76) = 76\\,\\text{ms}\)

Step 5: Verify all alternative complete paths from \(S\) to \(T\).
To ensure completeness, we evaluate the duration of all candidate paths:
Paths bypassing \(D\):
- Via \(B\):
  \(S\\to B\\to E\\to F\\to T: 18 + 26 + 8 + 20 = 72\\,\\text{ms}\)
  \(S\\to B\\to E\\to T: 18 + 26 + 24 = 68\\,\\text{ms}\)
- Via \(A\\to C\):
  \(S\\to A\\to C\\to E\\to F\\to T: 14 + 9 + 17 + 8 + 20 = 68\\,\\text{ms}\)
  \(S\\to A\\to C\\to E\\to T: 14 + 9 + 17 + 24 = 64\\,\\text{ms}\)
  \(S\\to A\\to C\\to F\\to T: 14 + 9 + 21 + 20 = 64\\,\\text{ms}\)
- Via direct \(S\\to C\):
  \(S\\to C\\to E\\to F\\to T: 11 + 17 + 8 + 20 = 56\\,\\text{ms}\)
  \(S\\to C\\to E\\to T: 11 + 17 + 24 = 52\\,\\text{ms}\)
  \(S\\to C\\to F\\to T: 11 + 21 + 20 = 52\\,\\text{ms}\)

Paths through \(D\):
- Through \(A\\to D\) (earliest arrival \(36\\,\\text{ms}\)):
  \(S\\to A\\to D\\to T: 14 + 22 + 28 = 64\\,\\text{ms}\)
  \(S\\to A\\to D\\to F\\to T: 14 + 22 + 19 + 20 = 75\\,\\text{ms}\)
  \(S\\to A\\to D\\to E\\to T: 14 + 22 + 12 + 24 = 72\\,\\text{ms}\)
  \(S\\to A\\to D\\to E\\to F\\to T: 14 + 22 + 12 + 8 + 20 = 76\\,\\text{ms}\)
- Through \(B\\to D\) (earliest arrival \(33\\,\\text{ms}\)):
  \(S\\to B\\to D\\to T: 18 + 15 + 28 = 61\\,\\text{ms}\)
  \(S\\to B\\to D\\to F\\to T: 18 + 15 + 19 + 20 = 72\\,\\text{ms}\)
  \(S\\to B\\to D\\to E\\to T: 18 + 15 + 12 + 24 = 69\\,\\text{ms}\)
  \(S\\to B\\to D\\to E\\to F\\to T: 18 + 15 + 12 + 8 + 20 = 73\\,\\text{ms}\)

The global maximum duration across all paths is \(76\\,\\text{ms}\).

Step 6: Identify the critical path and state the final result.
The unique path achieving the maximum total duration of \(76\\,\\text{ms}\) is:
\(S\\to A\\to D\\to E\\to F\\to T\)
with total latency:
\(14 + 22 + 12 + 8 + 20 = 76\\,\\text{ms}\)

Final Answer: 76"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        card = page.locator("div.rosetta-card:has-text('Enter the Golden Solution')")
        textarea = card.locator("textarea")
        
        print("Filling Golden Solution textarea...", flush=True)
        await textarea.focus()
        await textarea.fill(GOLDEN_SOLUTION_TEXT)
        await asyncio.sleep(0.5)
        
        val = await textarea.input_value()
        print(f"Filled length: {len(val)}", flush=True)
        
        # Click Continue using evaluate
        res = await page.evaluate('''() => {
            const card = document.querySelector("div.rosetta-card:has(h4, h3, h2)");
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.textContent.trim() === 'Continue');
            if (btn) {
                btn.click();
                return 'Clicked Continue';
            }
            return 'Continue button not found';
        }''')
        print("Continue click result:", res, flush=True)
        await asyncio.sleep(1.5)
        
        # Check next card
        card_info = await page.evaluate('''() => {
            const card = document.querySelector('div.rosetta-card');
            if (!card) return 'No card';
            const h = card.querySelector('h1, h2, h3, h4, h5, h6');
            return {
                heading: h ? h.innerText.trim() : null,
                text: card.innerText.slice(0, 300).replace(/\\n+/g, ' '),
                buttons: Array.from(card.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean)
            };
        }''')
        print("Next card info:", card_info, flush=True)

if __name__ == "__main__":
    asyncio.run(main())
