import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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
    browser, page = get_task_page(p)

    for i in range(20):
        if page.locator("button").count() > 5:
            break
        page.wait_for_timeout(500)

    # Dismiss timer modal if present
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        print("Dismissing timer modal...")
        modal_btn.first.click()
        page.wait_for_timeout(500)

    # Find the Start button under Feedback
    start_btn = page.locator("button:has-text('Start')").first
    print("Start button visible:", start_btn.is_visible())
    if start_btn.is_visible():
        print("Clicking Start under Feedback finding...")
        start_btn.click()
        page.wait_for_timeout(1500)

    page.screenshot(path="scratch/after_start_click_feedback.png")
    print("Saved scratch/after_start_click_feedback.png")

    # Inspect what elements appeared
    info = page.evaluate("""() => {
        const textareas = Array.from(document.querySelectorAll('textarea')).map(t => ({
            value: t.value.slice(0, 100),
            visible: t.offsetParent !== null,
            rect: t.getBoundingClientRect()
        }));
        const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            visible: b.offsetParent !== null
        }));
        return { textareas, buttons };
    }""")
    print("Textareas found:", info['textareas'])
    
    # If a textarea is visible, fill it with DESC_EXPANDED
    ta = page.locator("textarea").first
    if ta.count() > 0 and ta.is_visible():
        print("Found description textarea! Filling with 432-word description...")
        ta.fill(DESC_EXPANDED)
        page.wait_for_timeout(500)
        page.evaluate(f"""() => {{
            const el = document.querySelector('textarea');
            if (el) {{
                el.value = {DESC_EXPANDED!r};
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}""")
        page.wait_for_timeout(500)
        
        # Look for Save or Submit or Done button
        sub_btn = page.locator("button:has-text('Save'), button:has-text('Submit'), button:has-text('Done'), button:has-text('Continue')").first
        if sub_btn.is_visible():
            print(f"Clicking button: {sub_btn.inner_text()}...")
            sub_btn.click()
            page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_desc_saved.png")
    print("Saved scratch/after_desc_saved.png")

    body_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body_text.splitlines() if ln.strip()]
    print("\n--- Last 30 lines of page text ---")
    for ln in lines[-30:]:
        print(" ", ln)
