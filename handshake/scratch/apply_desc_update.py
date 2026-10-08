import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

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

print(f"Expanded description word count: {len(DESC_EXPANDED.split())} words")

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # 1. Dismiss modal
    print("Checking for Start timer modal...")
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0:
        box = st_btn.first.bounding_box()
        if box:
            print("Clicking Start timer button at", box)
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 2. Check if textarea is open
    ta = page.locator("textarea").first
    if not ta.is_visible():
        print("Textarea not open, clicking Edit on description...")
        clicked = page.evaluate("""() => {
            const all = Array.from(document.querySelectorAll('*'));
            const descHeader = all.find(el => el.innerText && el.innerText.includes('Write a detailed description') && el.children.length === 0);
            if (!descHeader) return false;
            let p = descHeader;
            while (p && p !== document.body) {
                const btn = p.querySelector('button[aria-label="Edit this step"]');
                if (btn) {
                    btn.click();
                    return true;
                }
                p = p.parentElement;
            }
            return false;
        }""")
        print("Clicked edit button:", clicked)
        page.wait_for_timeout(1000)

    # 3. Fill textarea
    print("Filling textarea...")
    ta = page.locator("textarea").first
    ta.scroll_into_view_if_needed()
    ta.fill(DESC_EXPANDED)
    page.wait_for_timeout(500)

    # Dispatch input/change events
    page.evaluate(f"""() => {{
        const ta = document.querySelector('textarea');
        if (ta) {{
            ta.value = {DESC_EXPANDED!r};
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}""")
    page.wait_for_timeout(500)

    # 4. Click the arrow-up commit button next to Cancel
    commit_res = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button found" };
        const parent = cancelBtn.parentElement;
        const buttons = Array.from(parent.querySelectorAll('button'));
        const arrowBtn = buttons.find(b => b !== cancelBtn);
        if (arrowBtn) {
            arrowBtn.click();
            return { success: true };
        }
        return { error: "No arrow button next to Cancel" };
    }""")
    print("Commit result:", commit_res)
    page.wait_for_timeout(2000)

    # 5. Click top Save
    top_save = page.locator("button:has-text('Save')").first
    if top_save.is_visible():
        print("Clicking top Save...")
        top_save.click()
        page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_desc_saved.png")
    print("Screenshot saved to scratch/after_desc_saved.png")
