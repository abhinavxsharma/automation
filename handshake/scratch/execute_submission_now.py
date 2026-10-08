import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome


def handle_modals(page):
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        print("Dismissing Start timer modal...")
        st_btn.click()
        page.wait_for_timeout(1000)


ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("text=Project Lumière", timeout=15000)
    page.wait_for_timeout(1000)

    # 1. Dismiss initial timer modal if present
    handle_modals(page)

    # 2. Verify readiness
    readiness = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const subBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        const fbIdx = bodyText.indexOf('Feedback');
        const sidebar = fbIdx !== -1 ? bodyText.slice(fbIdx, fbIdx + 300).replace(/\\n+/g, ' ') : '';
        return {
            hasSubmitBtn: !!subBtn,
            submitDisabled: subBtn ? subBtn.disabled : true,
            sidebar
        };
    }""")
    print("Pre-submission readiness:\n", json.dumps(readiness, indent=2))

    if not readiness["hasSubmitBtn"] or readiness["submitDisabled"]:
        print("ERROR: Submit task button is not ready or disabled!")
        sys.exit(1)

    # 3. Click 'Submit task' button via JS to prevent pointer events interception
    clicked_submit = page.evaluate("""() => {
        const subBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        if (subBtn && !subBtn.disabled) {
            subBtn.scrollIntoView({ behavior: 'instant', block: 'center' });
            subBtn.click();
            return true;
        }
        return false;
    }""")
    print("Clicked Submit task button:", clicked_submit)
    page.wait_for_timeout(2000)

    # 4. Check for dialogs (e.g. Confirm time, Are you sure, etc.)
    dialog_info = page.evaluate("""() => {
        const dialog = document.querySelector(\"[role='dialog'], [role='alertdialog']\");
        if (!dialog) return null;
        
        const btns = Array.from(dialog.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            classes: b.className
        }));

        return {
            text: dialog.innerText,
            btns
        };
    }""")
    print("Dialog after Submit task click:\n", json.dumps(dialog_info, indent=2))

    if dialog_info:
        # Check if it's the timer modal or a submission confirmation modal
        dialog_text = dialog_info["text"]
        if "Start timer" in dialog_text and "00:00" in dialog_text:
            print("Encountered timer dialog, dismissing and re-checking for submit dialog...")
            handle_modals(page)
            page.wait_for_timeout(1000)

            # Re-click Submit task if needed
            page.evaluate("""() => {
                const subBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
                if (subBtn && !subBtn.disabled) subBtn.click();
            }""")
            page.wait_for_timeout(2000)

        # Now check if a submission confirmation modal appeared (e.g. Confirm time, Submit, etc.)
        confirmed = page.evaluate("""() => {
            const dialog = document.querySelector(\"[role='dialog'], [role='alertdialog']\");
            if (!dialog) return { noDialog: true };
            
            // Look for confirm / submit buttons
            const btns = Array.from(dialog.querySelectorAll('button'));
            const confirmBtn = btns.find(b => {
                const t = b.innerText.trim().toLowerCase();
                return t === 'confirm time' || t === 'confirm' || t === 'submit' || t === 'yes, submit' || t.includes('submit');
            });
            
            if (confirmBtn) {
                confirmBtn.click();
                return { clickedConfirm: true, text: confirmBtn.innerText.trim() };
            }
            return { noConfirmBtnFound: true, btns: btns.map(b => b.innerText.trim()) };
        }""")
        print("Confirmation result:\n", json.dumps(confirmed, indent=2))
        page.wait_for_timeout(3000)

    # 5. Check post-submission state
    post_state = page.evaluate("""() => {
        return {
            url: window.location.href,
            title: document.title,
            bodySnippet: document.body.innerText.slice(0, 800)
        };
    }""")
    print("\n--- POST-SUBMISSION STATE ---")
    print("URL:", post_state["url"])
    print("Title:", post_state["title"])
    print("Body snippet:\n", post_state["bodySnippet"])

    page.screenshot(path="handshake/scratch/final_post_submission.png")
    print("\nSaved screenshot to handshake/scratch/final_post_submission.png")
