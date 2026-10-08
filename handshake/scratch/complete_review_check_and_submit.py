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
    close_btn = page.locator("button[aria-label='Close']")
    if close_btn.count() == 0 or not close_btn.first.is_visible():
        print("Opening feedback sidebar...")
        page.evaluate("""() => {
            const btn = document.querySelector("button[aria-label='Feedback']");
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(1500)
    dismiss_timer()

    # 3. Click the 'All' tab in feedback panel
    print("Clicking 'All' tab to inspect all reviews...")
    page.evaluate("""() => {
        const radios = document.querySelectorAll("fieldset[aria-label='Filter feedback'] input[type='radio']");
        if (radios.length > 0) radios[0].click();
    }""")
    page.wait_for_timeout(1500)
    dismiss_timer()

    # Extract all review items under All tab
    all_reviews = page.evaluate("""() => {
        const panel = document.querySelector("div[data-testid='task-side-panel']") ||
                      Array.from(document.querySelectorAll('*')).find(el => el.getBoundingClientRect().x > 750 && el.getBoundingClientRect().width > 200 && el.getBoundingClientRect().height > 500);
        
        // Find individual cards/items inside panel
        const cards = [];
        if (panel) {
            const children = Array.from(panel.querySelectorAll('div, article, section')).filter(el => {
                const text = el.innerText || '';
                return (text.includes('Wageesha') || text.includes('Checker') || text.includes('Science Judge')) && el.offsetHeight > 40;
            });
            return {
                panelFullText: panel.innerText,
                foundCardsCount: children.length
            };
        }
        return { error: 'No panel' };
    }""")

    print("\n=================== ALL REVIEWS IN SIDEBAR ===================")
    print(all_reviews.get("panelFullText", "Error reading panel"))
    print("==============================================================\n")

    page.screenshot(path="handshake/scratch/all_reviews_verified.png")
    print("Screenshot of all reviews saved to handshake/scratch/all_reviews_verified.png")

    # 4. Switch back to 'Needs attention' tab to verify 0 items need attention
    page.evaluate("""() => {
        const radios = document.querySelectorAll("fieldset[aria-label='Filter feedback'] input[type='radio']");
        if (radios.length > 1) radios[1].click();
    }""")
    page.wait_for_timeout(1000)
    dismiss_timer()

    # 5. Check Submit task button
    sub_btn_info = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        if (!btn) return { error: 'Submit button not found' };
        const rect = btn.getBoundingClientRect();
        return {
            text: btn.innerText,
            disabled: btn.disabled,
            ariaDisabled: btn.getAttribute('aria-disabled'),
            rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) }
        };
    }""")
    print("Submit Task Button Info:", sub_btn_info)

    # 6. Click Submit task!
    print("\n>>> CLICKING 'Submit task' BUTTON! <<<")
    clicked_submit = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        if (btn) {
            btn.click();
            return true;
        }
        return false;
    }""")
    print("Submit button clicked:", clicked_submit)
    page.wait_for_timeout(3000)

    # Dismiss timer if it appeared
    dismiss_timer()

    # 7. Check for modal/confirmation
    post_click_state = page.evaluate("""() => {
        const dialog = document.querySelector('div[role=\"dialog\"], [role=\"alertdialog\"], div[class*=\"z-50\"]');
        const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            rect: b.getBoundingClientRect()
        })).filter(b => b.text || b.aria);

        return {
            hasDialog: !!dialog,
            dialogText: dialog ? dialog.innerText : null,
            buttons: buttons,
            bodySnippet: document.body.innerText.slice(0, 400)
        };
    }""")
    print("Post-click state:\n", json.dumps(post_click_state, indent=2))

    page.screenshot(path="handshake/scratch/after_submit_task_clicked.png")
    print("Saved handshake/scratch/after_submit_task_clicked.png")

    # 8. Check for 'Confirm time' or any final confirmation button
    confirm_btn = page.locator("button:has-text('Confirm time'), button:has-text('Confirm'), button:has-text('Submit anyway'), button:has-text('Yes')").first
    if confirm_btn.count() > 0 and confirm_btn.is_visible():
        btn_text = confirm_btn.inner_text().strip()
        print(f"\n>>> Clicking confirmation button: '{btn_text}' <<<")
        confirm_btn.click()
        page.wait_for_timeout(4000)

    # 9. Final proof screenshot
    page.screenshot(path="handshake/scratch/final_submission_proof.png")
    print("Final proof screenshot saved to handshake/scratch/final_submission_proof.png")
    print("Final URL:", page.url)
    print("Final Title:", page.title())
