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

    # 2. Check Disagree button on Science Judge card
    print("Checking Disagree button...")
    disagree_res = page.evaluate("""() => {
        const btn = document.querySelector("button[aria-label='Disagree']");
        if (btn) {
            btn.click();
            return { found: true, clicked: true };
        }
        return { found: false };
    }""")
    print("Disagree click result:", disagree_res)
    page.wait_for_timeout(1500)
    dismiss_timer()

    # 3. Check bottom button in sidebar
    bottom_btn_info = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button')).filter(b => {
            const r = b.getBoundingClientRect();
            return r.x > 750 && r.y > 600;
        });
        return btns.map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            disabled: b.disabled,
            ariaDisabled: b.getAttribute('aria-disabled'),
            rect: b.getBoundingClientRect()
        }));
    }""")
    print("Bottom buttons:", bottom_btn_info)

    # 4. If button is 'Next', click 'Next'
    next_btn = page.locator("button:has-text('Next')")
    if next_btn.count() > 0 and next_btn.first.is_visible():
        print("Clicking 'Next' button...")
        page.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next' && b.getBoundingClientRect().x > 750);
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(2000)
        dismiss_timer()

    page.screenshot(path="handshake/scratch/after_next_or_disagree_step.png")
    print("Saved handshake/scratch/after_next_or_disagree_step.png")

    # 5. Check sidebar state and Submit task button
    sidebar_state = page.evaluate("""() => {
        const rightContainer = Array.from(document.querySelectorAll('*')).find(el => {
            const r = el.getBoundingClientRect();
            return r.x > 740 && r.width > 200 && r.height > 500;
        });
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        
        return {
            text: rightContainer ? rightContainer.innerText : 'None',
            hasSubmitBtn: !!submitBtn,
            submitDisabled: submitBtn ? submitBtn.disabled : null,
            submitAriaDisabled: submitBtn ? submitBtn.getAttribute('aria-disabled') : null
        };
    }""")
    print("\n=== SIDEBAR STATE ===")
    print("Text:\n", sidebar_state["text"])
    print("Has Submit button:", sidebar_state["hasSubmitBtn"])
    print("Submit disabled:", sidebar_state["submitDisabled"])
    print("Submit ariaDisabled:", sidebar_state["submitAriaDisabled"])

    # 6. If Submit task button is present, click it!
    if sidebar_state["hasSubmitBtn"]:
        print("\n>>> CLICKING 'Submit task'! <<<")
        page.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(3000)
        dismiss_timer()

        # Check for confirmation modal (e.g. Confirm time)
        confirm_state = page.evaluate("""() => {
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
        print("Confirmation dialog state:\n", json.dumps(confirm_state, indent=2))
        page.screenshot(path="handshake/scratch/after_submit_task_live.png")

        # Click Confirm time if visible
        confirm_btn = page.locator("button:has-text('Confirm time'), button:has-text('Confirm'), button:has-text('Submit anyway'), button:has-text('Yes')").first
        if confirm_btn.count() > 0 and confirm_btn.is_visible():
            btn_txt = confirm_btn.inner_text().strip()
            print(f">>> Found confirmation button '{btn_txt}', clicking... <<<")
            confirm_btn.click()
            page.wait_for_timeout(4000)

        page.screenshot(path="handshake/scratch/task_submitted_final_success.png")
        print("Final submission screenshot saved to handshake/scratch/task_submitted_final_success.png")
        print("Final Page URL:", page.url)
        print("Final Page Title:", page.title())
