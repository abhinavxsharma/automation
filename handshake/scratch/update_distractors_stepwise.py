import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

def update_distractor(page, distractor_num, target_val):
    # distractor_num is 1 to 5. Button index is 17 + distractor_num
    btn_idx = 17 + distractor_num
    print(f"\n================ Updating Distractor #{distractor_num} to: {target_val} ================")
    
    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(1000)
    
    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        st_btn.first.click()
        page.wait_for_timeout(1000)

    # Cancel any lingering open editor
    cancel_btn = page.locator("button:has-text('Cancel')")
    if cancel_btn.count() > 0 and cancel_btn.first.is_visible():
        cancel_btn.first.click()
        page.wait_for_timeout(1000)

    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    target_btn = edit_btns[btn_idx]
    target_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    target_btn.click()
    page.wait_for_timeout(1000)

    ta = page.locator("textarea[placeholder='Plausible-but-wrong answer text']").first
    print(f"Distractor #{distractor_num} old val: {repr(ta.input_value())}")
    ta.fill(target_val)
    page.wait_for_timeout(500)
    print(f"Distractor #{distractor_num} new val: {repr(ta.input_value())}")

    # Submit
    submitted = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return false;
        const sub = cancelBtn.parentElement.querySelector("button[aria-label='Submit']");
        if (sub) {
            sub.click();
            return true;
        }
        return false;
    }""")
    print("Submitted:", submitted)
    page.wait_for_timeout(2500)

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Distractor 1 is already $(A+\overline{B})C$
    # Update Distractor 2
    update_distractor(page, 2, "$C$")

    # Update Distractor 3
    update_distractor(page, 3, "$A+BC$")

    # Update Distractor 4
    update_distractor(page, 4, "$AC$")

    # Update Distractor 5
    update_distractor(page, 5, "$AB+C$")

    # Final verification of all 5
    page.wait_for_timeout(2000)
    info = page.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        const res = [];
        for (let i = 18; i <= 22; i++) {
            const btn = editBtns[i];
            if (!btn) continue;
            let card = btn.parentElement;
            while (card && !card.getAttribute('data-block-id') && !card.classList.contains('border') && card !== document.body) {
                card = card.parentElement;
            }
            res.push({
                num: i - 17,
                hasKaTeX: !!card.querySelector('.katex'),
                text: card.innerText.trim().replace(/\\n+/g, ' ')
            });
        }
        return res;
    }""")
    print("\n--- FINAL DISTRACTORS VERIFICATION ---")
    for r in info:
        print(f"Distractor #{r['num']} (KaTeX={r['hasKaTeX']}): {r['text']}")

    page.screenshot(path="handshake/scratch/all_distractors_final.png")
    print("Screenshot saved to handshake/scratch/all_distractors_final.png")
