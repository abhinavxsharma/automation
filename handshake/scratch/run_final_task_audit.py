import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("text=Project Lumière", timeout=15000)

    # 1. Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # 2. Click Save to ensure any pending changes are saved
    page.evaluate("""() => {
        const topSave = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (topSave && !topSave.disabled) topSave.click();
    }""")
    page.wait_for_timeout(1500)

    # 3. Full page audit
    audit = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Edit this step']\"));
        
        function getStep(idx) {
            const b = btns[idx];
            if (!b) return null;
            let card = b.closest('[data-block-id]') || b.parentElement;
            return {
                idx,
                blockId: card ? card.getAttribute('data-block-id') : null,
                hasKaTeX: !!(card && card.querySelector('.katex')),
                text: card ? card.innerText.trim() : ''
            };
        }

        const bodyText = document.body.innerText;
        const fbIdx = bodyText.indexOf('Feedback');
        const sidebar = fbIdx !== -1 ? bodyText.slice(fbIdx, fbIdx + 500) : 'None';

        const subBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');

        return {
            totalEditBtns: btns.length,
            step0_subdomain: getStep(0),
            step1_img_source: getStep(1),
            step7_prompt: getStep(7),
            step9_final_answer: getStep(9),
            step10_format: getStep(10),
            step13_failure_select: getStep(13),
            step14_error_type: getStep(14),
            distractor1: getStep(18),
            distractor2: getStep(19),
            distractor3: getStep(20),
            distractor4: getStep(21),
            distractor5: getStep(22),
            step23_qc: getStep(23),
            sidebarText: sidebar,
            canSubmit: !!(subBtn && !subBtn.disabled)
        };
    }""")

    print("=================== COMPREHENSIVE TASK AUDIT ===================")
    print("Total steps:", audit["totalEditBtns"])
    print(f"Step 0 (Subdomain): {audit['step0_subdomain']['text'][:60]}")
    print(f"Step 1 (Source): {audit['step1_img_source']['text'][:60]}")
    print(f"\nStep 7 (Prompt):\n{audit['step7_prompt']['text'][:200]}...")
    print(f"\nStep 9 (Final Answer): KaTeX={audit['step9_final_answer']['hasKaTeX']}")
    print(f"Text: {audit['step9_final_answer']['text'].replace(chr(10), ' ')}")
    print(f"\nStep 10 (Format): {audit['step10_format']['text'].replace(chr(10), ' ')}")
    print(f"\nDistractors (All KaTeX):")
    for d_name in ["distractor1", "distractor2", "distractor3", "distractor4", "distractor5"]:
        d = audit[d_name]
        print(f"  {d_name} (KaTeX={d['hasKaTeX']}): {d['text'].replace(chr(10), ' ')}")
    print(f"\nStep 23 (QC Resolution):\n{audit['step23_qc']['text']}")
    print(f"\nSidebar Text:\n{audit['sidebarText']}")
    print(f"\nSubmit task button enabled: {audit['canSubmit']}")
    print("================================================================")

    page.screenshot(path="handshake/scratch/final_verified_full_audit.png")
    print("Saved screenshot to handshake/scratch/final_verified_full_audit.png")
