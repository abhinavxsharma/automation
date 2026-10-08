import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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
    browser, page = get_task_page(p)

    for i in range(20):
        if page.locator("button").count() > 5:
            break
        page.wait_for_timeout(500)

    # 1. Dismiss timer modal
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        print("Clicking Start timer...")
        modal_btn.first.click()
        page.wait_for_timeout(1000)

    # 2. Find Golden Solution input
    print("Finding Golden Solution input...")
    inp = page.locator("textarea, [contenteditable='true'], input[placeholder*='typing']").first
    print("Input count:", inp.count())
    if inp.count() > 0:
        print("Filling Golden Solution...")
        inp.fill(GOLDEN_SOLUTION, force=True)
        page.wait_for_timeout(500)
        # Also trigger input/change events
        page.evaluate(f"""() => {{
            const el = document.querySelector("textarea, [contenteditable='true'], input[placeholder*='typing']");
            if (el) {{
                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
                    el.value = {GOLDEN_SOLUTION!r};
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }} else {{
                    el.innerText = {GOLDEN_SOLUTION!r};
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}
        }}""")
        page.wait_for_timeout(500)

    # 3. Click Continue
    cont = page.locator("button:has-text('Continue')").first
    if cont.is_visible():
        print("Clicking Continue...")
        cont.click()
        page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_golden_solution_filled.png")
    print("Saved scratch/after_golden_solution_filled.png")

    body_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body_text.splitlines() if ln.strip()]
    print("\n--- Last 30 lines of page text ---")
    for ln in lines[-30:]:
        print(" ", ln)
