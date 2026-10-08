import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

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

with sync_playwright() as p:
    ctx, pg = get_page(p)
    ta = pg.locator("textarea[placeholder='Start typing...']").first
    print("Filling Science Judge Justification...")
    ta.fill(JUSTIFICATION_TEXT, force=True)
    time.sleep(0.5)
    
    pg.evaluate(f"""(j) => {{
        const el = document.querySelector("textarea[placeholder='Start typing...']");
        if (el) {{
            el.value = j;
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}
    }}""", JUSTIFICATION_TEXT)
    time.sleep(0.5)
    
    cont_btn = pg.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(3)
    
    pg.screenshot(path="scratch/after_sj_justification.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_sj_justification.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 35 lines of page text ---")
    for ln in lines[-35:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
