import sys
import time

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

JUSTIFICATION = (
    "The model failed to correctly trace the directed topological critical path of the graph "
    "due to multiple crossing edges. Specifically, the planar crossing between directed edges "
    "(C, F) and (D, E) caused the model to swap their numerical latency labels: it misassigned the "
    "latency of 21 ms (which belongs to edge C -> F) to edge (D, E), which in reality has a latency "
    "of only 12 ms. Consequently, in Step 2 of its evaluation, the model calculated the earliest "
    "completion time of node E as L(E) = max(44, 40, 36 + 21) = 57 ms instead of the true value "
    "max(44, 40, 36 + 12) = 48 ms. Propagating this error forward, it computed L(F) = 57 + 8 = 65 ms "
    "and L(T) = 65 + 20 = 85 ms, returning an erroneous final answer of 85 ms instead of the ground "
    "truth critical path duration of 76 ms (an 11.8% error)."
)

DESC_EXPANDED = (
    "The figure displays a directed acyclic graph (DAG) representing a parallel computation "
    "task-dependency pipeline. The graph is laid out on a clean white background and consists of "
    "eight distinctly labeled circular nodes: an entry task node S on the far left, intermediate "
    "task nodes A, B, C, D, E, and F in the interior, and a terminal exit task node T on the far right. "
    "Each node is drawn as a filled circle outlined in bold dark navy border with its uppercase "
    "alphabetic identifier centered in the circle.\n\n"
    "Precedence constraints between tasks are represented by fifteen directed edges, each drawn as a "
    "solid navy blue arrow pointing from predecessor node u to successor node v with a prominent "
    "triangular arrowhead at the perimeter of the destination node circle. Accompanying each directed "
    "edge is a bold red numerical integer enclosed within a white rectangular badge with rounded corners "
    "and a thin gray border, denoting the execution and transmission latency along that dependency link "
    "in milliseconds (ms).\n\n"
    "The complete set of directed edges and their labeled latencies is as follows:\n"
    "- From entry node S: edge (S, A) directed to node A with latency 14 ms, edge (S, B) directed to "
    "node B with latency 18 ms, and edge (S, C) directed to node C with latency 11 ms.\n"
    "- From node A: edge (A, C) directed to node C with latency 9 ms, and edge (A, D) directed downward-right "
    "to node D with latency 22 ms.\n"
    "- From node B: edge (B, D) directed to node D with latency 15 ms, and diagonal edge (B, E) directed "
    "upward-right to node E with latency 26 ms.\n"
    "- From node C: edge (C, E) directed to node E with latency 17 ms, and edge (C, F) directed downward-right "
    "to node F with latency 21 ms.\n"
    "- From node D: edge (D, E) directed upward-right to node E with latency 12 ms, horizontal edge (D, F) "
    "directed to node F with latency 19 ms, and edge (D, T) directed downward-right to terminal node T with "
    "latency 28 ms.\n"
    "- From node E: vertical edge (E, F) directed downward to node F with latency 8 ms, and edge (E, T) "
    "directed downward-right to terminal node T with latency 24 ms.\n"
    "- From node F: edge (F, T) directed upward-right to terminal node T with latency 20 ms.\n\n"
    "Multiple edges cross each other in the two-dimensional planar layout: edge (S, C) crosses edge (A, D); "
    "edge (B, E) crosses edge (A, D); edge (C, F) crosses edge (D, E); and edge (D, T) crosses vertical edge (E, F)."
)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    for _ in range(10):
        t = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Model Failure Justification" in t or len(t) > 200:
            break
        time.sleep(0.5)

    # 1. Fill Failure Justification
    print("Filling Model Failure Justification...")
    inp = page.locator("textarea, input[placeholder='Start typing...'], div[contenteditable='true']").first
    inp.fill(JUSTIFICATION, force=True)
    page.wait_for_timeout(500)

    # Trigger events via JS
    page.evaluate(f"""() => {{
        const el = document.querySelector("textarea, input[placeholder='Start typing...'], [contenteditable='true']");
        if (el) {{
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
                el.value = {JUSTIFICATION!r};
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }} else {{
                el.innerText = {JUSTIFICATION!r};
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        }}
    }}""")
    page.wait_for_timeout(500)

    # Click Continue on Justification
    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue on Justification...")
    cont_btn.click(force=True)
    page.wait_for_timeout(2000)

    # 2. Check if Start button on finding is visible
    start_btn = page.locator("button:has-text('Start')").first
    if start_btn.is_visible():
        print("Clicking Start on Image Description finding...")
        start_btn.click(force=True)
        page.wait_for_timeout(1500)

        # Look for textarea to update description
        ta = page.locator("textarea").first
        if ta.is_visible():
            print("Updating Image Description with 432-word description...")
            ta.fill(DESC_EXPANDED)
            page.wait_for_timeout(500)
            sub = page.locator("button:has-text('Submit'), button:has-text('Save'), button:has-text('Continue')").first
            if sub.is_visible():
                sub.click(force=True)
                page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_justification_and_desc.png")
    print("Saved scratch/after_justification_and_desc.png")

    new_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in new_text.splitlines() if ln.strip()]
    print("\n--- Active Step Context ---")
    for ln in lines[-35:]:
        print(" ", ln)
