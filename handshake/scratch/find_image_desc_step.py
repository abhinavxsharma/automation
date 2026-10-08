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

    # 1. Dismiss timer modal
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        print("Dismissing timer modal...")
        modal_btn.first.click()
        page.wait_for_timeout(500)

    # 2. Find which edit pencil corresponds to Image Description
    target_idx = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label="Edit this step"]'));
        for (let i = 0; i < btns.length; i++) {
            const b = btns[i];
            let cur = b.parentElement;
            let text = '';
            for (let step = 0; step < 5 && cur; step++) {
                text += cur.innerText + ' ';
                cur = cur.parentElement;
            }
            if (text.includes('15 directed edges') || text.includes('directed acyclic graph (DAG) representing')) {
                return i;
            }
        }
        return -1;
    }""")

    print(f"Target 'Edit this step' index: {target_idx}")
    if target_idx != -1:
        edit_btn = page.locator('button[aria-label="Edit this step"]').nth(target_idx)
        print("Scrolling edit button into view and clicking...")
        edit_btn.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        edit_btn.click()
        page.wait_for_timeout(1500)

        page.screenshot(path="scratch/after_desc_edit_clicked.png")
        print("Saved scratch/after_desc_edit_clicked.png")

        # Now find the active textarea
        ta = page.locator("textarea").first
        if ta.count() > 0 and ta.is_visible():
            print("Found description textarea! Updating with 432-word description...")
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

            # Click Continue or Save or Update
            cont = page.locator("button:has-text('Continue'), button:has-text('Save'), button:has-text('Update')").first
            if cont.is_visible():
                print(f"Clicking {cont.inner_text()}...")
                cont.click()
                page.wait_for_timeout(2000)

        page.screenshot(path="scratch/after_desc_updated_now.png")
        print("Saved scratch/after_desc_updated_now.png")
    else:
        print("Could not find matching edit button by text! Inspecting nearby texts for each button...")
        btn_texts = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('button[aria-label="Edit this step"]')).map((b, i) => {
                let cur = b.parentElement;
                let text = '';
                for (let s = 0; s < 4 && cur; s++) {
                    text += cur.innerText + ' ';
                    cur = cur.parentElement;
                }
                return { index: i, snippet: text.slice(0, 100).replace(/\\n/g, ' ') };
            });
        }""")
        for bt in btn_texts:
            print(" ", bt)
