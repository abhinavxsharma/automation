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

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Dismiss timer modal if present
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Start timer'));
        if (btn) btn.click();
        const overlays = Array.from(document.querySelectorAll('div[class*="z-50"]'));
        overlays.forEach(o => o.remove());
    }""")

    # 1. Click edit on description
    clicked = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const target = all.find(e => e.innerText && e.innerText.includes('minimum of 200 words') && e.children.length === 0);
        if (!target) return false;
        let c = target;
        while (c && c !== document.body) {
            const btn = c.querySelector('button[aria-label="Edit this step"]');
            if (btn) {
                btn.scrollIntoView({ behavior: 'instant', block: 'center' });
                btn.click();
                return true;
            }
            c = c.parentElement;
        }
        return false;
    }""")
    print("Clicked edit description:", clicked)

    # 2. Wait for visible textarea
    ta = page.locator("textarea:visible").first
    ta.wait_for(state="visible", timeout=8000)
    print("Textarea visible! Filling...")
    ta.fill(DESC_TEXT)
    page.wait_for_timeout(500)
    print("Filled. Chars:", len(ta.input_value()), "Words:", len(ta.input_value().split()))

    # 3. Click Submit button
    submit_btn = page.locator("button[aria-label='Submit']:visible").first
    submit_btn.wait_for(state="visible", timeout=5000)
    submit_btn.click(force=True)
    print("Clicked Submit button.")
    page.wait_for_timeout(2000)

    # 4. Click top Save
    save_btn = page.locator("button:has-text('Save')").first
    save_btn.click(force=True)
    print("Clicked top Save.")
    page.wait_for_timeout(3000)

    # 5. Check resulting text
    desc_result = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const target = all.find(e => e.innerText && e.innerText.includes('minimum of 200 words') && e.children.length === 0);
        let c = target;
        for (let i = 0; i < 5; i++) if (c.parentElement) c = c.parentElement;
        return {
            textLength: c.innerText.length,
            snippet: c.innerText.slice(-300)
        };
    }""")
    print("Result after save:", desc_result)
    page.screenshot(path="scratch/clean_desc_saved.png")
