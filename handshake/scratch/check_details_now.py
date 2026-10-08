import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(1000)

    # Dismiss timer if visible
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(500)

    res = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        
        function getCardInfo(idx) {
            const b = btns[idx];
            if (!b) return null;
            let p = b.parentElement;
            while (p && !p.getAttribute('data-block-id') && p !== document.body) {
                p = p.parentElement;
            }
            return {
                idx,
                blockId: p ? p.getAttribute('data-block-id') : null,
                hasKaTeX: !!(p && p.querySelector('.katex')),
                text: p ? p.innerText : ''
            };
        }
        
        return {
            totalBtns: btns.length,
            step7: getCardInfo(7),
            step9: getCardInfo(9),
            step10: getCardInfo(10),
            distractors: [getCardInfo(18), getCardInfo(19), getCardInfo(20), getCardInfo(21), getCardInfo(22)],
            step23: getCardInfo(23)
        };
    }""")
    print("Total btns:", res["totalBtns"])
    print("--- STEP 7 (Prompt) ---")
    print(res["step7"]["text"] if res["step7"] else "None")
    print("\n--- STEP 9 (Final Answer) ---")
    print(res["step9"]["text"] if res["step9"] else "None")
    print("KaTeX:", res["step9"]["hasKaTeX"] if res["step9"] else False)
    print("\n--- STEP 10 (Format) ---")
    print(res["step10"]["text"] if res["step10"] else "None")
    print("\n--- DISTRACTORS ---")
    for d in res["distractors"]:
        if d:
            print(f"Distractor #{d['idx']-17} (KaTeX={d['hasKaTeX']}): {d['text']}")
    print("\n--- STEP 23 (QC Resolution) ---")
    print(res["step23"]["text"] if res["step23"] else "None")
