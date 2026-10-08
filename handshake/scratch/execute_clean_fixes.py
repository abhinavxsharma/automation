import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

DESC_TEXT = (
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

JUSTIFICATION_TEXT = (
    "The Science Judge flag (AMBIGUOUS_PROMPT) is a clear automated false positive resulting from text parser misalignment.\n\n"
    "1. Source of the Quote:\n"
    "The quote cited by the Science Judge (\"The prompt can only be solved with the information in the image\") is NOT taken from the author's prompt. "
    "Rather, it is the verbatim label of the platform's pre-submission checklist checkbox located directly below the prompt input block. "
    "The automated judge erroneously ingested this checklist string rather than the actual prompt body.\n\n"
    "2. Explicit Computational Objective:\n"
    "The actual submitted prompt explicitly defines the computational problem and objective:\n"
    "\"The figure shows a task-dependency directed acyclic graph (DAG) representing a parallel computation pipeline. "
    "Tasks are nodes S, A, B, C, D, E, F, T, where S is entry and T is terminal. Directed edges (u,v) represent precedence with latency in milliseconds (ms). "
    "Assuming tasks start immediately once all predecessors complete, determine the critical path duration (maximum latency from S to T). "
    "Answer in ms as a 2 significant figure number without units.\"\n\n"
    "3. Deterministic Ground Truth Solution:\n"
    "The objective is the standard, well-posed Critical Path Method (CPM) / longest-path problem on a DAG. Using topological dynamic programming:\n"
    "- L(S) = 0\n"
    "- L(A) = 0 + 14 = 14\n"
    "- L(B) = 0 + 18 = 18\n"
    "- L(C) = max(0 + 11, 14 + 9) = 23\n"
    "- L(D) = max(14 + 22, 18 + 15) = max(36, 33) = 36\n"
    "- L(E) = max(23 + 17, 18 + 26, 36 + 12) = max(40, 44, 48) = 48\n"
    "- L(F) = max(23 + 21, 36 + 19, 48 + 8) = max(44, 55, 56) = 56\n"
    "- L(T) = max(36 + 28, 48 + 24, 56 + 20) = max(64, 72, 76) = 76\n\n"
    "The critical path is uniquely S -> A -> D -> E -> F -> T with latency 76 ms. The answer 76 is strictly determined, mathematically sound, and entirely unambiguous."
)


def dismiss_modal_if_open(page):
    try:
        modal_btn = page.locator("button:has-text('Start timer')")
        if modal_btn.count() > 0:
            box = modal_btn.first.bounding_box()
            if box:
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                page.wait_for_timeout(500)
    except Exception as e:
        print("Modal dismiss error:", e)


with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_timeout(1000)

    dismiss_modal_if_open(page)

    # =========================================================================
    # STEP 1: FIX IMAGE DESCRIPTION
    # =========================================================================
    print("--- 1. Fixing Image Description ---")

    # Click edit button for Image Description
    edit_desc_clicked = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const descHeader = all.find(el => el.innerText && el.innerText.includes('Write a detailed description of your image') && el.children.length === 0);
        if (!descHeader) return false;
        let p = descHeader;
        while (p && p !== document.body) {
            const btn = p.querySelector('button[aria-label="Edit this step"]');
            if (btn) {
                btn.scrollIntoView({ behavior: 'instant', block: 'center' });
                btn.click();
                return true;
            }
            p = p.parentElement;
        }
        return false;
    }""")
    print("Clicked edit description:", edit_desc_clicked)
    page.wait_for_timeout(1000)
    dismiss_modal_if_open(page)

    # Locate the visible textarea
    ta = page.locator("textarea").first
    ta.wait_for(state="visible", timeout=5000)
    print("Textarea visible! Clearing and replacing value...")

    # Clear textarea completely and set new value
    page.evaluate(f"""() => {{
        const ta = document.querySelector('textarea');
        if (ta) {{
            ta.value = {DESC_TEXT!r};
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}""")
    page.wait_for_timeout(500)

    # Click the commit button (arrow next to Cancel)
    desc_committed = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button" };
        const parent = cancelBtn.parentElement;
        const arrowBtn = Array.from(parent.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (arrowBtn) {
            arrowBtn.click();
            return { success: true };
        }
        return { error: "No arrow button" };
    }""")
    print("Description committed:", desc_committed)
    page.wait_for_timeout(2000)
    dismiss_modal_if_open(page)

    # =========================================================================
    # STEP 2: FIX SCIENCE JUDGE JUSTIFICATION
    # =========================================================================
    print("--- 2. Fixing Science Judge Justification ---")

    # Click edit button for Science Judge step
    edit_sj_clicked = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const sjHeader = all.find(el => el.innerText && el.innerText.includes('Pay close attention to the Science Judge') && el.children.length === 0);
        if (!sjHeader) return false;
        let p = sjHeader;
        while (p && p !== document.body) {
            const btn = p.querySelector('button[aria-label="Edit this step"]');
            if (btn) {
                btn.scrollIntoView({ behavior: 'instant', block: 'center' });
                btn.click();
                return true;
            }
            p = p.parentElement;
        }
        return false;
    }""")
    print("Clicked edit Science Judge:", edit_sj_clicked)
    page.wait_for_timeout(1000)
    dismiss_modal_if_open(page)

    # Locate textarea for Science Judge
    ta = page.locator("textarea").first
    ta.wait_for(state="visible", timeout=5000)
    print("Science Judge textarea visible! Clearing and replacing value...")

    page.evaluate(f"""() => {{
        const ta = document.querySelector('textarea');
        if (ta) {{
            ta.value = {JUSTIFICATION_TEXT!r};
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}""")
    page.wait_for_timeout(500)

    # Click the commit button (arrow next to Cancel)
    sj_committed = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button" };
        const parent = cancelBtn.parentElement;
        const arrowBtn = Array.from(parent.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (arrowBtn) {
            arrowBtn.click();
            return { success: true };
        }
        return { error: "No arrow button" };
    }""")
    print("Science Judge committed:", sj_committed)
    page.wait_for_timeout(2000)
    dismiss_modal_if_open(page)

    # =========================================================================
    # STEP 3: TOP SAVE
    # =========================================================================
    print("--- 3. Clicking top Save ---")
    save_result = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const saveBtn = btns.find(b => b.innerText.trim() === 'Save');
        if (saveBtn) {
            saveBtn.click();
            return 'Clicked Save';
        }
        return 'No Save button';
    }""")
    print("Save result:", save_result)
    page.wait_for_timeout(3000)

    page.screenshot(path="scratch/after_both_fixes.png")
    print("Screenshot saved to scratch/after_both_fixes.png")
