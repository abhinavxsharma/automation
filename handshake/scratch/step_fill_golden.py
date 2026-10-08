import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

GOLDEN_SOLUTION = (
    "Step 1: Identify all 8 nodes S, A, B, C, D, E, F, T and all directed edge latencies in milliseconds from the DAG figure:\n"
    "- Precedence constraints from S: (S, A) = 14 ms, (S, B) = 18 ms, (S, C) = 11 ms.\n"
    "- Precedence constraints from A: (A, C) = 9 ms, (A, D) = 22 ms.\n"
    "- Precedence constraints from B: (B, D) = 15 ms, (B, E) = 26 ms.\n"
    "- Precedence constraints from C: (C, E) = 17 ms, (C, F) = 21 ms.\n"
    "- Precedence constraints from D: (D, E) = 12 ms, (D, F) = 19 ms, (D, T) = 28 ms.\n"
    "- Precedence constraints from E: (E, F) = 8 ms, (E, T) = 24 ms.\n"
    "- Precedence constraints from F: (F, T) = 20 ms.\n\n"
    "Step 2: Note the topological ordering of the DAG vertices: S, A, B, C, D, E, F, T. Evaluate the earliest completion times (maximum path latencies from source S) for each intermediate node.\n\n"
    "Step 3: Evaluate path prefixes arriving at node D:\n"
    "- Path prefix via A: S -> A -> D has duration 14 + 22 = 36 ms.\n"
    "- Path prefix via B: S -> B -> D has duration 18 + 15 = 33 ms.\n"
    "Thus, the longest path prefix to reach node D is max(36, 33) = 36 ms, achieved via S -> A -> D.\n\n"
    "Step 4: From node D, evaluate the downstream subpaths reaching terminal node T:\n"
    "- Direct exit D -> T: total latency is 36 + 28 = 64 ms.\n"
    "- Subpath D -> F -> T: total latency is 36 + 19 + 20 = 75 ms.\n"
    "- Subpath D -> E -> T: total latency is 36 + 12 + 24 = 72 ms.\n"
    "- Subpath D -> E -> F -> T: total latency is 36 + 12 + 8 + 20 = 76 ms.\n\n"
    "Step 5: Compare against all alternative paths in the DAG that bypass node D:\n"
    "- Paths via B -> E: S -> B -> E -> F -> T has latency 18 + 26 + 8 + 20 = 72 ms; S -> B -> E -> T has latency 18 + 26 + 24 = 68 ms.\n"
    "- Paths via node C: S -> A -> C -> E -> F -> T has latency 14 + 9 + 17 + 8 + 20 = 68 ms; S -> C -> E -> F -> T has latency 11 + 17 + 8 + 20 = 56 ms; S -> C -> F -> T has latency 11 + 21 + 20 = 52 ms.\n"
    "Across all possible directed paths from S to T, the maximum duration is 76 ms along path S -> A -> D -> E -> F -> T.\n\n"
    "Final Answer:\n"
    "76"
)

with sync_playwright() as p:
    ctx, pg = get_page(p)
    ta = pg.locator("textarea[placeholder='Start typing...']").first
    print("Filling Golden Solution into textarea...")
    ta.fill(GOLDEN_SOLUTION, force=True)
    time.sleep(0.5)
    
    pg.evaluate(f"""(sol) => {{
        const el = document.querySelector("textarea[placeholder='Start typing...']");
        if (el) {{
            el.value = sol;
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}""", GOLDEN_SOLUTION)
    time.sleep(0.5)
    
    cont_btn = pg.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(3)
    
    pg.screenshot(path="scratch/after_golden_filled.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_golden_filled.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 35 lines of page text ---")
    for ln in lines[-35:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
