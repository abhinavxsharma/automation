import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

def dismiss_timer_modal(page):
    dismissed = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Start timer'));
        if (btn) {
            btn.click();
            return true;
        }
        return false;
    }""")
    if dismissed:
        print("Dismissed Start timer modal via JS.")
        page.wait_for_timeout(1000)

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_timeout(2000)
    dismiss_timer_modal(page)

    # Cancel any open editor
    cancel_btn = page.locator("button:has-text('Cancel')")
    if cancel_btn.count() > 0 and cancel_btn.first.is_visible():
        cancel_btn.first.click()
        page.wait_for_timeout(1000)

    dismiss_timer_modal(page)

    # Find edit button for Final Answer (index 9)
    print("\n--- Updating Final Answer to $(A+B)C$ ---")
    btn_info = page.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        const btn = editBtns[9];
        if (!btn) return false;
        btn.scrollIntoView({ behavior: 'instant', block: 'center' });
        btn.click();
        return true;
    }""")
    print("Clicked Edit on Final Answer:", btn_info)
    page.wait_for_timeout(1500)
    dismiss_timer_modal(page)

    # Find the textarea/input for Final Answer
    ta = page.locator("textarea[placeholder*='answer' i], textarea, input[type='text']").first
    print("Old Final Answer value:", repr(ta.input_value()))
    ta.fill("$(A+B)C$")
    page.wait_for_timeout(500)
    print("New Final Answer value:", repr(ta.input_value()))

    # Click Submit in the Final Answer card
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
    print("Submitted Final Answer:", submitted)
    page.wait_for_timeout(2500)

    # Verify Final Answer card
    fa_status = page.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        const btn = editBtns[9];
        let card = btn.parentElement;
        while (card && !card.getAttribute('data-block-id') && !card.classList.contains('border') && card !== document.body) {
            card = card.parentElement;
        }
        return {
            hasKaTeX: !!card.querySelector('.katex'),
            text: card.innerText.trim().replace(/\\n+/g, ' ')
        };
    }""")
    print("Final Answer status:", fa_status)
    page.screenshot(path="handshake/scratch/fa_katex_done.png")
