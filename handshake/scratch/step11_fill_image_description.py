import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

IMAGE_DESC = """The figure displays a task-dependency directed acyclic graph (DAG) representing a parallel computation pipeline laid out on a clean white background. The graph comprises eight circular task nodes labeled S, A, B, C, D, E, F, and T. Each node is drawn as a pale cream-colored circular disk outlined with a solid, distinct black border, with its bold uppercase alphabetic label centered within the circle. Entry node S is positioned at the far left, intermediate nodes A, B, C, D, E, and F occupy the interior columns, and terminal exit node T is situated at the far right.

Precedence constraints between tasks are depicted by fifteen solid dark navy blue directed arrows extending between node perimeters, each terminating in a sharp triangular arrowhead pointing to the destination task node. Every directed edge is accompanied by a bold dark red numerical integer enclosed within an on-edge white rectangular badge with rounded corners and a thin gray border, denoting the link latency in milliseconds (ms).

The complete set of fifteen directed edges and their respective labeled latencies is:
- Directed edge (S, A) from node S to node A with latency 14 ms.
- Directed edge (S, B) from node S to node B with latency 18 ms.
- Directed edge (S, C) from node S to node C with latency 11 ms.
- Directed edge (A, C) from node A to node C with latency 9 ms.
- Directed edge (A, D) from node A to node D with latency 22 ms.
- Directed edge (B, D) from node B to node D with latency 15 ms.
- Directed edge (B, E) from node B to node E with latency 26 ms.
- Directed edge (C, E) from node C to node E with latency 17 ms.
- Directed edge (C, F) from node C to node F with latency 21 ms.
- Directed edge (D, E) from node D to node E with latency 12 ms.
- Directed edge (D, F) from node D to node F with latency 19 ms.
- Directed edge (D, T) from node D to node T with latency 28 ms.
- Directed edge (E, F) from node E to node F with latency 8 ms.
- Directed edge (E, T) from node E to node T with latency 24 ms.
- Directed edge (F, T) from node F to node T with latency 20 ms."""

with sync_playwright() as p:
    browser, page = get_task_page(p)

    ta = page.locator("textarea[placeholder='Start typing...'], textarea").first
    ta.scroll_into_view_if_needed()
    time.sleep(0.5)
    print("Filling Image Description...")
    ta.fill("")
    page.wait_for_timeout(200)
    ta.fill(IMAGE_DESC)
    page.wait_for_timeout(300)
    page.evaluate("""(desc) => {
        const ta = document.querySelector("textarea[placeholder='Start typing...']") || document.querySelector("textarea");
        if (ta) {
            ta.value = desc;
            ta.dispatchEvent(new Event('input', { bubbles: true }));
            ta.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""", IMAGE_DESC)
    time.sleep(1)

    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(2)

    page.screenshot(path="scratch/after_image_desc_continue.png")
    print("Screenshot saved to scratch/after_image_desc_continue.png")
