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

    # 1. Dismiss timer modal if present
    timer_btn = page.locator("button:has-text('Start timer')")
    if timer_btn.count() > 0 and timer_btn.first.is_visible():
        print("Dismissing timer modal...")
        timer_btn.first.click()
        page.wait_for_timeout(1000)

    # 2. Check if description textarea is currently visible
    ta = page.locator("textarea").first
    if not ta.is_visible():
        print("Textarea not open, clicking Edit on description...")
        # Find edit button
        page.evaluate("""() => {
            const all = Array.from(document.querySelectorAll('*'));
            const descHeader = all.find(el => el.innerText && el.innerText.includes('Write a detailed description') && el.children.length === 0);
            if (!descHeader) return;
            let p = descHeader;
            while (p && p !== document.body) {
                const btn = p.querySelector('button[aria-label="Edit this step"]');
                if (btn) {
                    btn.click();
                    return;
                }
                p = p.parentElement;
            }
        }""")
        page.wait_for_timeout(1000)

    # 3. Fill the textarea
    print("Filling textarea with expanded description...")
    ta = page.locator("textarea").first
    ta.scroll_into_view_if_needed()
    ta.fill(DESC_EXPANDED)
    page.wait_for_timeout(500)

    # Dispatch events
    page.evaluate(f"""() => {{
        const ta = document.querySelector('textarea');
        if (ta) {{
            ta.value = {DESC_EXPANDED!r};
            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
            ta.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}""")
    page.wait_for_timeout(500)

    # 4. Find the submit/save button near the textarea
    # Usually next to Cancel button: button with arrow up or submit
    save_info = page.evaluate("""() => {
        const ta = document.querySelector('textarea');
        if (!ta) return { error: "No textarea" };
        const card = ta.closest('div.w-full, section, div[class*="container"]') || ta.parentElement.parentElement;
        const btns = Array.from(card.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            disabled: b.disabled,
            className: b.className
        }));
        return { btns };
    }""")
    print("Buttons near textarea:", save_info)

    # Click the non-cancel button inside the card (the save/submit button)
    clicked_save = page.evaluate("""() => {
        const ta = document.querySelector('textarea');
        if (!ta) return false;
        const card = ta.closest('div.w-full, section, div[class*="container"]') || ta.parentElement.parentElement;
        // The save button is the button that is not 'Cancel'
        const btns = Array.from(card.querySelectorAll('button')).filter(b => b.innerText.trim() !== 'Cancel' && b.offsetParent !== null);
        if (btns.length > 0) {
            btns[btns.length - 1].click();
            return true;
        }
        return false;
    }""")
    print("Clicked save button:", clicked_save)
    page.wait_for_timeout(2500)

    page.screenshot(path="scratch/after_step1_desc_saved.png")
    print("Screenshot saved to scratch/after_step1_desc_saved.png")
