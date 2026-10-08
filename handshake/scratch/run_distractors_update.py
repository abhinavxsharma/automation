import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

def handle_modals(page):
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        print("Dismissing Start timer modal...")
        st_btn.first.click()
        page.wait_for_timeout(1000)

    rt_btn = page.locator("button[aria-label='Resume timer']")
    if rt_btn.count() > 0 and rt_btn.first.is_visible():
        print("Clicking Resume timer...")
        rt_btn.first.click()
        page.wait_for_timeout(1000)

def update_single_distractor(page, num, val):
    print(f"\n>>> Updating Distractor #{num} to {val}")
    handle_modals(page)
    
    # Cancel any lingering editor
    cancel_btn = page.locator("button:has-text('Cancel')")
    if cancel_btn.count() > 0 and cancel_btn.first.is_visible():
        cancel_btn.first.click()
        page.wait_for_timeout(1000)

    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    target_btn = edit_btns[17 + num]
    target_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    
    # Check modals before click
    handle_modals(page)
    target_btn.click()
    page.wait_for_timeout(1000)

    # If start timer modal popped up right after click, dismiss and click again
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        st_btn.first.click()
        page.wait_for_timeout(1000)
        target_btn.click()
        page.wait_for_timeout(1000)

    ta = page.locator("textarea[placeholder='Plausible-but-wrong answer text']").first
    print(f"Distractor #{num} old: {repr(ta.input_value())}")
    ta.fill(val)
    page.wait_for_timeout(500)
    print(f"Distractor #{num} new: {repr(ta.input_value())}")

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
    print(f"Distractor #{num} submitted: {submitted}")
    page.wait_for_timeout(2000)

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(2000)

    # Update Distractor 2
    update_single_distractor(page, 2, "$C$")

    # Update Distractor 3
    update_single_distractor(page, 3, "$A+BC$")

    # Update Distractor 4
    update_single_distractor(page, 4, "$AC$")

    # Update Distractor 5
    update_single_distractor(page, 5, "$AB+C$")

    # Final verification
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
    print("\n--- FINAL DISTRACTORS STATUS ---")
    for r in info:
        print(f"Distractor #{r['num']} (KaTeX={r['hasKaTeX']}): {r['text']}")

    page.screenshot(path="handshake/scratch/all_5_distractors_done.png")
    print("Saved screenshot to handshake/scratch/all_5_distractors_done.png")
