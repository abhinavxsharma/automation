import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

NEW_DESC = """The image displays a directed graph laid out horizontally on a white canvas. The graph consists of eight circular nodes labeled S, A, B, C, D, E, F, and T. Each node is rendered as a pale yellow filled circular disk with a thin black circular outline, with its uppercase letter identifier centered in black font. Entry node S is positioned on the left side of the canvas, intermediate nodes A, B, C, D, E, and F are positioned across the middle area, and terminal exit node T is situated on the right side.

Precedence constraints are displayed as fifteen dark blue directed arrows connecting the nodes. Each arrow line features a prominent triangular arrowhead at the destination node boundary indicating the direction of traversal. Alongside each arrow line, a numerical weight badge is displayed as a bold red integer enclosed inside a white rounded rectangular box with a light outline.

The complete list of directed edges and their labeled numerical weights shown in the figure is:
- Directed edge (S, A) from node S to node A with weight 14.
- Directed edge (S, B) from node S to node B with weight 18.
- Directed edge (S, C) from node S to node C with weight 11.
- Directed edge (A, C) from node A to node C with weight 9.
- Directed edge (A, D) from node A to node D with weight 22.
- Directed edge (B, D) from node B to node D with weight 15.
- Directed edge (B, E) from node B to node E with weight 26.
- Directed edge (C, E) from node C to node E with weight 17.
- Directed edge (C, F) from node C to node F with weight 21.
- Directed edge (D, E) from node D to node E with weight 12.
- Directed edge (D, F) from node D to node F with weight 19.
- Directed edge (D, T) from node D to node T with weight 28.
- Directed edge (E, F) from node E to node F with weight 8.
- Directed edge (E, T) from node E to node T with weight 24.
- Directed edge (F, T) from node F to node T with weight 20.

All eight node labels and fifteen edge weight values are plainly visible and directly readable from the diagram."""

NEW_JUSTIFICATION = """The model exhibited a label-to-element mis-binding error. The model correctly identified all graph nodes and directed edge connectivity, but mis-bound the numerical latency badges at the planar crossing of directed edges $(C, F)$ and $(D, E)$. Specifically, it swapped their numerical latency labels: it attached the latency of $21\\,\\text{ms}$ (which belongs to directed edge $C \\to F$) to edge $D \\to E$ (which has a true latency of $12\\,\\text{ms}$), and attached $12\\,\\text{ms}$ to $C \\to F$. Consequently, in Step 2 of its topological dynamic programming evaluation, the model calculated the earliest completion time of node $E$ as $L(E) = \\max(44, 40, 36 + 21) = 57\\,\\text{ms}$ instead of the true value $\\max(44, 40, 36 + 12) = 48\\,\\text{ms}$. Propagating this mis-bound label forward, it computed $L(F) = 57 + 8 = 65\\,\\text{ms}$ and $L(T) = 65 + 20 = 85\\,\\text{ms}$, returning an erroneous final answer of $85\\,\\text{ms}$ instead of the ground truth critical path duration of $76\\,\\text{ms}$ (an $11.8\\%$ error)."""

NEW_GOLDEN_SOLUTION = """Step 1: Identify all 8 nodes $S, A, B, C, D, E, F, T$ and directed edge latencies from the DAG figure: $(S, A) = 14\\,\\text{ms}$, $(S, B) = 18\\,\\text{ms}$, $(S, C) = 11\\,\\text{ms}$; $(A, C) = 9\\,\\text{ms}$, $(A, D) = 22\\,\\text{ms}$; $(B, D) = 15\\,\\text{ms}$, $(B, E) = 26\\,\\text{ms}$; $(C, E) = 17\\,\\text{ms}$, $(C, F) = 21\\,\\text{ms}$; $(D, E) = 12\\,\\text{ms}$, $(D, F) = 19\\,\\text{ms}$, $(D, T) = 28\\,\\text{ms}$; $(E, F) = 8\\,\\text{ms}$, $(E, T) = 24\\,\\text{ms}$; $(F, T) = 20\\,\\text{ms}$.

Step 2: Note the topological ordering $S, A, B, C, D, E, F, T$. Define earliest completion time $L(v)$ as the maximum path latency from entry $S$, with base case $L(S) = 0\\,\\text{ms}$.

Step 3: Calculate the earliest completion time for node $A$ with incoming edge from $S$: $L(A) = L(S) + w(S, A) = 0 + 14 = 14\\,\\text{ms}$.

Step 4: Calculate the earliest completion time for node $B$ with incoming edge from $S$: $L(B) = L(S) + w(S, B) = 0 + 18 = 18\\,\\text{ms}$.

Step 5: Calculate the earliest completion time for node $C$ with incoming edges from $S$ and $A$: $L(C) = \\max(L(S) + w(S, C), L(A) + w(A, C)) = \\max(0 + 11, 14 + 9) = \\max(11, 23) = 23\\,\\text{ms}$.

Step 6: Calculate the earliest completion time for node $D$ with incoming edges from $A$ and $B$: $L(D) = \\max(L(A) + w(A, D), L(B) + w(B, D)) = \\max(14 + 22, 18 + 15) = \\max(36, 33) = 36\\,\\text{ms}$.

Step 7: Calculate the earliest completion time for node $E$ with incoming edges from $C$, $B$, and $D$: $L(E) = \\max(L(C) + w(C, E), L(B) + w(B, E), L(D) + w(D, E)) = \\max(23 + 17, 18 + 26, 36 + 12) = \\max(40, 44, 48) = 48\\,\\text{ms}$.

Step 8: Calculate the earliest completion time for node $F$ with incoming edges from $C$, $D$, and $E$: $L(F) = \\max(L(C) + w(C, F), L(D) + w(D, F), L(E) + w(E, F)) = \\max(23 + 21, 36 + 19, 48 + 8) = \\max(44, 55, 56) = 56\\,\\text{ms}$.

Step 9: Calculate the earliest completion time for terminal node $T$ (critical path duration) with incoming edges from $D$, $E$, and $F$: $L(T) = \\max(L(D) + w(D, T), L(E) + w(E, T), L(F) + w(F, T)) = \\max(36 + 28, 48 + 24, 56 + 20) = \\max(64, 72, 76) = 76\\,\\text{ms}$.

Final Answer: 76"""


def update_step(page, btn_idx, new_value, name):
    print(f"\n--- Updating Step {btn_idx} ({name}) ---")
    # Click edit button
    click_res = page.evaluate("""(idx) => {
        const btns = Array.from(document.querySelectorAll('button[aria-label="Edit this step"]'));
        if (btns[idx]) {
            btns[idx].scrollIntoView({ behavior: 'instant', block: 'center' });
            btns[idx].click();
            return { success: true };
        }
        return { error: `Button ${idx} not found` };
    }""", btn_idx)
    print(f"Click edit: {click_res}")
    time.sleep(1.5)

    # Set value using property descriptor
    fill_res = page.evaluate("""(val) => {
        const tas = Array.from(document.querySelectorAll('textarea')).filter(t => t.getBoundingClientRect().height > 0);
        if (tas.length > 0) {
            const ta = tas[0];
            ta.scrollIntoView({ behavior: 'instant', block: 'center' });
            const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
            setter.call(ta, val);
            ta.dispatchEvent(new Event('input', { bubbles: true }));
            ta.dispatchEvent(new Event('change', { bubbles: true }));
            return { success: true, len: val.length };
        }
        return { error: "No textarea visible" };
    }""", new_value)
    print(f"Fill textarea: {fill_res}")
    time.sleep(1)

    # Click commit arrow button
    commit_res = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button found" };
        const parent = cancelBtn.parentElement;
        const arrowBtn = Array.from(parent.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (arrowBtn) {
            arrowBtn.scrollIntoView({ behavior: 'instant', block: 'center' });
            arrowBtn.click();
            return { success: true };
        }
        return { error: "No commit arrow button found" };
    }""")
    print(f"Commit: {commit_res}")
    time.sleep(2)


with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # 1. Update Step 11 (Image Description)
    update_step(pg, 11, NEW_DESC, "Image Description")
    
    # 2. Update Step 15 (Model Failure Justification)
    update_step(pg, 15, NEW_JUSTIFICATION, "Model Failure Justification")
    
    # 3. Update Step 16 (Golden Solution)
    update_step(pg, 16, NEW_GOLDEN_SOLUTION, "Golden Solution")
    
    pg.screenshot(path="scratch/after_form_updates.png")
    print("Screenshot saved to scratch/after_form_updates.png")
