import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

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
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # 1. Dismiss modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Start timer'));
        if (btn) btn.click();
        const overlays = Array.from(document.querySelectorAll('div[class*="z-50"]'));
        overlays.forEach(o => o.remove());
    }""")

    # 2. Click edit Science Judge
    page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const target = all.find(e => e.innerText && e.innerText.includes('Pay close attention to the Science Judge') && e.children.length === 0);
        let c = target;
        while (c && c !== document.body) {
            const btn = c.querySelector('button[aria-label="Edit this step"]');
            if (btn) {
                btn.scrollIntoView({ behavior: 'instant', block: 'center' });
                btn.click();
                break;
            }
            c = c.parentElement;
        }
    }""")
    page.wait_for_timeout(1000)

    # 3. Fill textarea
    ta = page.locator("textarea:visible").first
    ta.wait_for(state="visible", timeout=5000)
    ta.fill(JUSTIFICATION_TEXT)
    page.wait_for_timeout(500)

    # 4. Inspect commit button
    btn_info = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button" };
        const buttons = Array.from(cancelBtn.parentElement.querySelectorAll('button'));
        const commitBtn = buttons.find(b => b !== cancelBtn);
        if (!commitBtn) return { error: "No commit button" };
        return {
            aria: commitBtn.getAttribute('aria-label'),
            disabled: commitBtn.disabled,
            ariaDisabled: commitBtn.getAttribute('aria-disabled'),
            rect: commitBtn.getBoundingClientRect()
        };
    }""")
    print("Commit button info:", btn_info)

    # 5. Click the commit button using its bounding box or JS click
    clicked = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return false;
        const commitBtn = Array.from(cancelBtn.parentElement.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (commitBtn) {
            commitBtn.click();
            return true;
        }
        return false;
    }""")
    print("Clicked commit button via JS:", clicked)
    page.wait_for_timeout(2000)

    # Check if textarea closed
    is_ta_visible = page.evaluate("() => !!document.querySelector('textarea:not([data-testid=\"stuck-report-context\"])')")
    print("Is textarea still in DOM?", is_ta_visible)

    # 6. Click top Save
    save_res = page.evaluate("""() => {
        const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (saveBtn) {
            saveBtn.click();
            return 'Clicked Save';
        }
        return 'No Save button';
    }""")
    print("Top save result:", save_res)
    page.wait_for_timeout(3000)

    # 7. Check text in page
    result = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const target = all.find(e => e.innerText && e.innerText.includes('Pay close attention to the Science Judge') && e.children.length === 0);
        let c = target;
        for (let i = 0; i < 5; i++) if (c && c.parentElement) c = c.parentElement;
        return {
            textLength: c ? c.innerText.length : 0,
            hasJustification: c ? c.innerText.includes('automated false positive') : false,
            snippet: c ? c.innerText.slice(0, 300) : ''
        };
    }""")
    print("Final Science Judge check:", result)
    page.screenshot(path="scratch/final_sj_check.png")
