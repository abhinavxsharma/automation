import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

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

    # Dismiss timer modal
    btn = page.locator("button:has-text('Start timer')").first
    box = btn.bounding_box()
    if box:
        print("Dismissing timer modal...")
        page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
        page.wait_for_timeout(1000)

    # Click Start button on finding in sidebar
    start_btn = page.locator("button:has-text('Start')").first
    if start_btn.is_visible():
        print("Clicking Start on Image Description finding...")
        start_btn.click(force=True)
        page.wait_for_timeout(1500)

    page.screenshot(path="scratch/after_click_start_finding.png")
    print("Saved scratch/after_click_start_finding.png")

    # Look for the description input / textarea
    tas = page.locator("textarea").all()
    print(f"Found {len(tas)} textareas")
    for i, t in enumerate(tas):
        print(f"  TA {i}: vis={t.is_visible()} val={t.input_value()[:60]}")

    if tas:
        # Find the one with description or first visible
        target_ta = next((t for t in tas if t.is_visible() and ("figure displays" in t.input_value() or "DAG" in t.input_value())), tas[0])
        print("Filling expanded 432-word description into textarea...")
        target_ta.fill(DESC_EXPANDED)
        page.wait_for_timeout(1000)

        # Look for Save / Submit / Continue button
        sub_btn = page.locator("button:has-text('Save'), button:has-text('Submit'), button:has-text('Continue')").first
        if sub_btn.is_visible():
            print("Clicking submit/save on updated description...")
            sub_btn.click(force=True)
            page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_desc_updated_clean.png")
    print("Saved scratch/after_desc_updated_clean.png")
