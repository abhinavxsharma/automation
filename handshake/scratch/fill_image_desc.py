import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

DESC = (
    "The figure displays a directed acyclic graph (DAG) representing a parallel computation "
    "task-dependency pipeline. It consists of 8 labeled nodes: entry node S, intermediate tasks "
    "A, B, C, D, E, F, and terminal exit node T. There are 15 directed edges with numerical latency "
    "weights in milliseconds (ms): (S, A) = 14 ms, (S, B) = 18 ms, (S, C) = 11 ms, (A, C) = 9 ms, "
    "(A, D) = 22 ms, (B, D) = 15 ms, (B, E) = 26 ms, (C, E) = 17 ms, (C, F) = 21 ms, (D, E) = 12 ms, "
    "(D, F) = 19 ms, (D, T) = 28 ms, (E, F) = 8 ms, (E, T) = 24 ms, and (F, T) = 20 ms. Several edges "
    "cross in the plane: edge (S, C) crosses edge (A, D); edge (B, E) crosses edge (A, D); edge (C, F) "
    "crosses edge (D, E); and edge (D, T) crosses edge (E, F)."
)

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer modal if present
    btn = page.locator("button:has-text('Start timer')").first
    box = btn.bounding_box()
    if box:
        print("Dismissing timer modal...")
        page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
        page.wait_for_timeout(1000)

    # Locate description input / textarea
    inp = page.locator("textarea, input[placeholder='Start typing...'], div[contenteditable='true']").first
    print("Filling Image Description...")
    inp.fill(DESC, force=True)
    page.wait_for_timeout(500)

    # Trigger events via JS if needed
    page.evaluate(f"""() => {{
        const el = document.querySelector("textarea, input[placeholder='Start typing...'], [contenteditable='true']");
        if (el) {{
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {{
                el.value = {DESC!r};
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }} else {{
                el.innerText = {DESC!r};
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        }}
    }}""")
    page.wait_for_timeout(500)

    # Click Continue
    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_desc_continue.png")
    print("Saved scratch/after_desc_continue.png")

    new_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in new_text.splitlines() if ln.strip()]
    print("\n--- Active Step After Description ---")
    for ln in lines[-30:]:
        print(" ", ln)
