import json
import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # 1. Dismiss timer modal
    def dismiss_timer():
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible():
            b = st.bounding_box()
            if b:
                print("Dismissing timer modal...")
                page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                page.wait_for_timeout(1000)

    dismiss_timer()

    # 2. Ensure feedback sidebar is open
    def ensure_sidebar():
        close_btn = page.locator("button[aria-label='Close']")
        if close_btn.count() == 0 or not close_btn.first.is_visible():
            print("Sidebar is closed. Opening via Feedback button...")
            page.evaluate("""() => {
                const btn = document.querySelector("button[aria-label='Feedback']");
                if (btn) btn.click();
            }""")
            page.wait_for_timeout(1500)
            dismiss_timer()
        print("Sidebar is now open.")

    ensure_sidebar()

    # 3. Check what is in the sidebar right now
    panel_state = page.evaluate("""() => {
        const panel = document.querySelector("div[data-testid='task-side-panel']") ||
                      Array.from(document.querySelectorAll('*')).find(el => el.getBoundingClientRect().x > 750 && el.getBoundingClientRect().width > 200 && el.getBoundingClientRect().height > 500);
        
        const disagreeBtn = document.querySelector("button[aria-label='Disagree']");
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next' && b.getBoundingClientRect().x > 750);
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task' && b.getBoundingClientRect().x > 750);

        return {
            text: panel ? panel.innerText : 'No panel',
            hasDisagree: !!disagreeBtn,
            hasNext: !!nextBtn,
            hasSubmit: !!submitBtn,
            nextDisabled: nextBtn ? nextBtn.disabled : null,
            submitDisabled: submitBtn ? submitBtn.disabled : null,
            submitAriaDisabled: submitBtn ? submitBtn.getAttribute('aria-disabled') : null
        };
    }""")

    print("\n=== INITIAL SIDEBAR STATE ===")
    print("Text:\n", panel_state["text"])
    print("hasDisagree:", panel_state["hasDisagree"])
    print("hasNext:", panel_state["hasNext"])
    print("hasSubmit:", panel_state["hasSubmit"])
    page.screenshot(path="handshake/scratch/step1_initial_sidebar.png")

    # 4. If disagree button is visible, click it!
    if panel_state["hasDisagree"]:
        print("\nClicking Disagree button on Science Judge card...")
        page.evaluate("""() => {
            const btn = document.querySelector("button[aria-label='Disagree']");
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(2000)
        dismiss_timer()

    # 5. Check if Next button is present and click it
    has_next = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next' && b.getBoundingClientRect().x > 750);
        if (btn) {
            btn.click();
            return true;
        }
        return false;
    }""")
    if has_next:
        print("Clicked 'Next' button!")
        page.wait_for_timeout(2000)
        dismiss_timer()

    page.screenshot(path="handshake/scratch/step2_after_next.png")

    # 6. Check sidebar state again
    panel_state_2 = page.evaluate("""() => {
        const panel = document.querySelector("div[data-testid='task-side-panel']") ||
                      Array.from(document.querySelectorAll('*')).find(el => el.getBoundingClientRect().x > 750 && el.getBoundingClientRect().width > 200 && el.getBoundingClientRect().height > 500);
        
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task' && b.getBoundingClientRect().x > 750);
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next' && b.getBoundingClientRect().x > 750);

        return {
            text: panel ? panel.innerText : 'No panel',
            hasNext: !!nextBtn,
            hasSubmit: !!submitBtn,
            submitDisabled: submitBtn ? submitBtn.disabled : null,
            submitAriaDisabled: submitBtn ? submitBtn.getAttribute('aria-disabled') : null
        };
    }""")
    print("\n=== STATE 2 AFTER NEXT/DISAGREE ===")
    print("Text:\n", panel_state_2["text"])
    print("hasNext:", panel_state_2["hasNext"])
    print("hasSubmit:", panel_state_2["hasSubmit"])
    print("submitDisabled:", panel_state_2["submitDisabled"])
    print("submitAriaDisabled:", panel_state_2["submitAriaDisabled"])

    # If it still has Next, click Next again (sometimes takes 2 clicks or advances)
    if panel_state_2["hasNext"] and not panel_state_2["hasSubmit"]:
        print("Clicking 'Next' again...")
        page.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next' && b.getBoundingClientRect().x > 750);
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(2000)
        dismiss_timer()

    # 7. CLICK 'Submit task'!
    clicked_submit = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task' && b.getBoundingClientRect().x > 750);
        if (btn) {
            btn.click();
            return true;
        }
        return false;
    }""")
    print("\n>>> Submitted Task Button Clicked:", clicked_submit, "<<<")
    page.wait_for_timeout(3000)
    dismiss_timer()

    page.screenshot(path="handshake/scratch/step3_after_submit_task.png")

    # 8. Check for confirmation modal (e.g. 'Confirm time')
    confirm_info = page.evaluate("""() => {
        const dialog = document.querySelector('div[role=\"dialog\"], [role=\"alertdialog\"], div[class*=\"z-50\"]');
        const btns = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            rect: b.getBoundingClientRect()
        })).filter(b => b.text || b.aria);

        return {
            hasDialog: !!dialog,
            dialogText: dialog ? dialog.innerText : null,
            buttons: btns
        };
    }""")
    print("\nConfirmation dialog info:\n", json.dumps(confirm_info, indent=2))

    # Click Confirm time if visible
    confirm_btn = page.locator("button:has-text('Confirm time'), button:has-text('Confirm'), button:has-text('Submit anyway'), button:has-text('Yes')").first
    if confirm_btn.count() > 0 and confirm_btn.is_visible():
        btn_txt = confirm_btn.inner_text().strip()
        print(f"\n>>> Found confirmation button: '{btn_txt}'. Clicking... <<<")
        confirm_btn.click()
        page.wait_for_timeout(5000)

    # 9. Final proof capture
    page.screenshot(path="handshake/scratch/step4_final_submitted_proof.png")
    print("\n================ FINAL DELIVERY STATE ================")
    print("URL:", page.url)
    print("Title:", page.title())
    print("Proof Screenshot: handshake/scratch/step4_final_submitted_proof.png")
    print("=======================================================")
