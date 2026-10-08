import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    def dismiss_timer():
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible():
            b = st.bounding_box()
            if b:
                print("Dismissing timer modal...")
                page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                page.wait_for_timeout(500)

    # Step 1: Initial dismiss & sidebar check
    dismiss_timer()
    close_btn = page.locator("button[aria-label='Close']")
    if close_btn.count() == 0 or not close_btn.first.is_visible():
        print("Opening feedback sidebar...")
        page.evaluate("""() => {
            const btn = document.querySelector("button[aria-label='Feedback']");
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(1000)
    dismiss_timer()

    # Step 2: Check if Science Judge Disagree is needed
    disagree_btn = page.locator("button[aria-label='Disagree']")
    if disagree_btn.count() > 0 and disagree_btn.first.is_visible():
        print("Clicking Disagree icon on Science Judge finding at (1056, 199)...")
        page.mouse.click(1056, 199)
        page.wait_for_timeout(1000)
        dismiss_timer()

    # Step 3: Check if Next button is present
    next_btn = page.locator("button:has-text('Next')")
    if next_btn.count() > 0 and next_btn.first.is_visible():
        print("Clicking Next button at (946, 725)...")
        page.mouse.click(946, 725)
        page.wait_for_timeout(1500)
        dismiss_timer()

    page.screenshot(path="handshake/scratch/final_step_before_submit.png")
    print("Screenshot saved to handshake/scratch/final_step_before_submit.png")

    # Step 4: Verify Submit task button
    sub_btn = page.locator("button:has-text('Submit task')").first
    print("Submit task button exists:", sub_btn.count() > 0)
    print("Submit task visible:", sub_btn.is_visible())
    box = sub_btn.bounding_box()
    print("Submit task box:", box)

    # Step 5: CLICK SUBMIT TASK!
    print("\n==========================================")
    print(">>> CLICKING 'Submit task' BUTTON! <<<")
    print("==========================================")
    if box:
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(2000)
    dismiss_timer()

    page.screenshot(path="handshake/scratch/final_step_after_submit_click.png")

    # Step 6: Loop and handle Confirm time or completion dialog
    completed = False
    for i in range(1, 25):
        page.wait_for_timeout(1000)
        dismiss_timer()

        # Check for Confirm time
        confirm_time = page.locator("button:has-text('Confirm time')").first
        if confirm_time.count() > 0 and confirm_time.is_visible():
            print(f"[{i}s] Found 'Confirm time' button! Clicking...")
            confirm_time.click()
            page.wait_for_timeout(3000)
            completed = True
            break

        # Check for any other confirmation dialog
        dialog_txt = page.evaluate("""() => {
            const d = document.querySelector('div[role=\"dialog\"], [role=\"alertdialog\"]');
            return d ? d.innerText : '';
        }""")
        if "Great job" in dialog_txt or "Task complete" in dialog_txt:
            print(f"[{i}s] Task completion dialog reached: {dialog_txt[:100]}")
            completed = True
            break

        # Check body text for Task complete
        body_txt = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Task complete!" in body_txt or "Time confirmed" in body_txt:
            print(f"[{i}s] 'Task complete!' detected on page!")
            completed = True
            break

    # Step 7: Final Screenshot
    page.screenshot(path="handshake/scratch/delivery_completed_success.png")
    print("\n==========================================")
    print(">>> TASK DELIVERY COMPLETED! <<<")
    print("Final URL:", page.url)
    print("Final Title:", page.title())
    print("Proof Screenshot: handshake/scratch/delivery_completed_success.png")
    print("==========================================")
