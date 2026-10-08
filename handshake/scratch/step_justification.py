import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

JUSTIFICATION = """The model failed to correctly trace the directed topological critical path of the graph due to multiple crossing edges. Specifically, the planar crossing between directed edges (C, F) and (D, E) caused the model to swap their numerical latency labels: it misassigned the latency of 21 ms (which belongs to edge C -> F) to edge (D, E), which in reality has a latency of only 12 ms. Consequently, in Step 2 of its evaluation, the model calculated the earliest completion time of node E as L(E) = max(44, 40, 36 + 21) = 57 ms instead of the true value max(44, 40, 36 + 12) = 48 ms. Propagating this error forward, it computed L(F) = 57 + 8 = 65 ms and L(T) = 65 + 20 = 85 ms, returning an erroneous final answer of 85 ms instead of the ground truth critical path duration of 76 ms (an 11.8% error)."""

with sync_playwright() as p:
    ctx, pg = get_page(p)
    ta = pg.locator("textarea").first
    print("Filling Model Failure Justification...")
    ta.fill(JUSTIFICATION, force=True)
    time.sleep(0.5)
    
    pg.evaluate(f"""(j) => {{
        const el = document.querySelector('textarea');
        if (el) {{
            el.value = j;
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}""", JUSTIFICATION)
    time.sleep(0.5)
    
    cont_btn = pg.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(3)
    
    pg.screenshot(path="scratch/after_justification_continue.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_justification.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 35 lines of page text ---")
    for ln in lines[-35:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
