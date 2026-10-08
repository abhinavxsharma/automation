import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

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

JUSTIFICATION_EXPANDED = (
    "The Science Judge flag (AMBIGUOUS_PROMPT) is a false positive caused by automated misparsing: "
    "the automated tool extracted the fourth pre-submission declaration checkbox ('The prompt can only "
    "be solved with the information in the image') as the prompt text, rather than evaluating the actual task prompt.\n\n"
    "The actual prompt text submitted is:\n"
    "'The figure shows a task-dependency directed acyclic graph (DAG) representing a parallel computation "
    "pipeline. Tasks are nodes $S, A, B, C, D, E, F, T$, where $S$ is entry and $T$ is terminal. Directed edges "
    "$(u, v)$ represent precedence with latency in milliseconds (\\text{ms}). Assuming tasks start immediately "
    "once all predecessors complete, determine the critical path duration (maximum latency from $S$ to $T$). "
    "Answer in ms as a 2 significant figure number without units. Intermediate calculations to 6 significant figures. "
    "Unstated constants to 4 significant figures.'\n\n"
    "As explicitly shown above, the prompt states a precise, unambiguous computational question: "
    "'determine the critical path duration (maximum latency from S to T). Answer in ms as a 2 significant figure number without units.' "
    "Under standard parallel DAG scheduling, tasks start as soon as all predecessors complete; thus the completion time "
    "of terminal node T is strictly governed by the longest directed path from entry node S to terminal node T. "
    "In this DAG, there are 15 directed edges with explicit latency weights, and the maximum latency path is uniquely "
    "S -> A -> D -> E -> F -> T with total latency 14 + 22 + 12 + 8 + 20 = 76 ms. The objective and ground truth "
    "answer 76 are completely determined, mathematically rigorous, self-contained, and solvable solely from the provided graph topology."
)

print(f"Description length: {len(DESC_EXPANDED.split())} words")
print(f"Justification length: {len(JUSTIFICATION_EXPANDED.split())} words")

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer if visible
    btn = page.locator("button:has-text('Start timer')").first
    if btn.is_visible():
        box = btn.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # ==========================================
    # STEP 1: FIX IMAGE DESCRIPTION
    # ==========================================
    print("\n--- STEP 1: FIX IMAGE DESCRIPTION ---")
    page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const descHeader = all.find(el => el.innerText && el.innerText.includes('Write a detailed description') && el.children.length === 0);
        if (!descHeader) return;
        let cur = descHeader;
        while (cur && cur !== document.body) {
            const btn = cur.querySelector('button[aria-label="Edit this step"]');
            if (btn) {
                btn.scrollIntoView({ behavior: 'instant', block: 'center' });
                btn.click();
                return;
            }
            cur = cur.parentElement;
        }
    }""")
    page.wait_for_timeout(1500)

    # Check if textarea is open
    ta = page.locator("textarea").first
    if ta.is_visible():
        print("Description textarea is visible. Filling...")
        ta.fill(DESC_EXPANDED)
        page.wait_for_timeout(500)
        page.evaluate(f"""() => {{
            const ta = document.querySelector('textarea');
            if (ta) {{
                ta.value = {DESC_EXPANDED!r};
                ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}""")
        page.wait_for_timeout(500)

        # Click the save button inside the textarea card
        clicked = page.evaluate("""() => {
            const ta = document.querySelector('textarea');
            if (!ta) return false;
            const card = ta.closest('div.w-full, section, div[class*="container"]') || ta.parentElement.parentElement;
            const btns = Array.from(card.querySelectorAll('button')).filter(b => b.innerText.trim() !== 'Cancel' && b.offsetParent !== null);
            if (btns.length > 0) {
                btns[btns.length - 1].click();
                return true;
            }
            return false;
        }""")
        print("Clicked description save button:", clicked)
        page.wait_for_timeout(2000)

    # ==========================================
    # STEP 2: FIX SCIENCE JUDGE JUSTIFICATION
    # ==========================================
    print("\n--- STEP 2: FIX SCIENCE JUDGE JUSTIFICATION ---")
    page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const sjHeader = all.find(el => el.innerText && el.innerText.includes('Pay close attention to the Science Judge') && el.children.length === 0);
        if (!sjHeader) return;
        let cur = sjHeader;
        while (cur && cur !== document.body) {
            const btn = cur.querySelector('button[aria-label="Edit this step"]');
            if (btn) {
                btn.scrollIntoView({ behavior: 'instant', block: 'center' });
                btn.click();
                return;
            }
            cur = cur.parentElement;
        }
    }""")
    page.wait_for_timeout(1500)

    # Check for textarea
    ta = page.locator("textarea").first
    if ta.is_visible():
        print("Science Judge justification textarea is visible. Filling...")
        ta.fill(JUSTIFICATION_EXPANDED)
        page.wait_for_timeout(500)
        page.evaluate(f"""() => {{
            const ta = document.querySelector('textarea');
            if (ta) {{
                ta.value = {JUSTIFICATION_EXPANDED!r};
                ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}""")
        page.wait_for_timeout(500)

        # Click save button
        clicked = page.evaluate("""() => {
            const ta = document.querySelector('textarea');
            if (!ta) return false;
            const card = ta.closest('div.w-full, section, div[class*="container"]') || ta.parentElement.parentElement;
            const btns = Array.from(card.querySelectorAll('button')).filter(b => b.innerText.trim() !== 'Cancel' && b.offsetParent !== null);
            if (btns.length > 0) {
                btns[btns.length - 1].click();
                return true;
            }
            return false;
        }""")
        print("Clicked Science Judge justification save button:", clicked)
        page.wait_for_timeout(2000)

    # Click top Save button
    top_save = page.locator("button:has-text('Save')").first
    if top_save.is_visible():
        print("Clicking top Save button...")
        top_save.click(force=True)
        page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_both_fixes_saved.png")
    print("Screenshot saved to scratch/after_both_fixes_saved.png")
