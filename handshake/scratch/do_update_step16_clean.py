import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

NEW_GOLDEN_SOLUTION = """Step 1: Identify all 8 nodes S, A, B, C, D, E, F, T and directed edge latencies from the DAG figure:
(S, A) = 14 ms, (S, B) = 18 ms, (S, C) = 11 ms;
(A, C) = 9 ms, (A, D) = 22 ms;
(B, D) = 15 ms, (B, E) = 26 ms;
(C, E) = 17 ms, (C, F) = 21 ms;
(D, E) = 12 ms, (D, F) = 19 ms, (D, T) = 28 ms;
(E, F) = 8 ms, (E, T) = 24 ms;
(F, T) = 20 ms.

Step 2: Note the topological ordering S, A, B, C, D, E, F, T. Define earliest completion time L(v) as maximum path latency from entry S, with base case L(S) = 0 ms.

Step 3: Calculate the earliest completion time for node A:
Incoming edge is from S:
L(A) = L(S) + w(S, A) = 0 + 14 = 14 ms.

Step 4: Calculate the earliest completion time for node B:
Incoming edge is from S:
L(B) = L(S) + w(S, B) = 0 + 18 = 18 ms.

Step 5: Calculate the earliest completion time for node C:
Incoming edges are from S and A:
L(C) = max(L(S) + w(S, C), L(A) + w(A, C)) = max(0 + 11, 14 + 9) = max(11, 23) = 23 ms.

Step 6: Calculate the earliest completion time for node D:
Incoming edges are from A and B:
L(D) = max(L(A) + w(A, D), L(B) + w(B, D)) = max(14 + 22, 18 + 15) = max(36, 33) = 36 ms.

Step 7: Calculate the earliest completion time for node E:
Incoming edges are from C, B, and D:
L(E) = max(L(C) + w(C, E), L(B) + w(B, E), L(D) + w(D, E)) = max(23 + 17, 18 + 26, 36 + 12) = max(40, 44, 48) = 48 ms.

Step 8: Calculate the earliest completion time for node F:
Incoming edges are from C, D, and E:
L(F) = max(L(C) + w(C, F), L(D) + w(D, F), L(E) + w(E, F)) = max(23 + 21, 36 + 19, 48 + 8) = max(44, 55, 56) = 56 ms.

Step 9: Calculate the earliest completion time for terminal node T (critical path duration):
Incoming edges are from D, E, and F:
L(T) = max(L(D) + w(D, T), L(E) + w(E, T), L(F) + w(F, T)) = max(36 + 28, 48 + 24, 56 + 20) = max(64, 72, 76) = 76 ms.

Final Answer: 76"""

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button", timeout=10000)
    
    # 1. Dismiss timer modal
    print("Dismissing modal...")
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)
    
    # 2. Click Edit on Step 16 (Golden Solution)
    res = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label=\"Edit this step\"]'));
        // Find Step 16 (Golden Solution)
        const target = btns.find(b => {
            const c = b.closest('div.flex-col, div[data-block-id], section') || b.parentElement;
            return c && c.innerText.toLowerCase().includes('golden solution');
        }) || btns[16];
        if (target) {
            target.scrollIntoView({ behavior: 'instant', block: 'center' });
            target.click();
            return { success: true };
        }
        return { error: "No edit button found" };
    }""")
    print("Clicked Edit Step 16:", res)
    page.wait_for_timeout(1500)
    
    # 3. Fill textarea using React setter
    fill_res = page.evaluate("""(val) => {
        const ta = document.querySelector('textarea');
        if (!ta) return { error: "No textarea found" };
        ta.scrollIntoView({ behavior: 'instant', block: 'center' });
        
        const setter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        setter.call(ta, val);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        return { success: true, valLength: ta.value.length };
    }""", NEW_GOLDEN_SOLUTION)
    print("Filled textarea result:", fill_res)
    page.wait_for_timeout(1000)
    
    # 4. Commit via arrow button
    commit_res = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button" };
        const parent = cancelBtn.parentElement;
        const arrowBtn = Array.from(parent.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (arrowBtn) {
            arrowBtn.scrollIntoView({ behavior: 'instant', block: 'center' });
            arrowBtn.click();
            return { success: true };
        }
        return { error: "No arrow button" };
    }""")
    print("Commit result:", commit_res)
    page.wait_for_timeout(2500)
    
    page.screenshot(path="scratch/step16_after_update.png")
    
    # 5. Check saved text
    saved_text = page.evaluate("""() => {
        const h = Array.from(document.querySelectorAll('h3, h4, div')).find(el => el.innerText && el.innerText.trim() === 'Enter the Golden Solution:');
        if (h) {
            const container = h.closest('div.border, div[data-block-id], section') || h.parentElement.parentElement;
            return container.innerText;
        }
        return 'Container not found';
    }""")
    print("\n=== SAVED GOLDEN SOLUTION ===")
    print(saved_text[:600])
