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

    dismiss_timer()

    # Listen to relevant network requests
    def on_response(resp):
        url = resp.url
        if any(k in url for k in ["submit", "task", "run", "annotation"]):
            try:
                body = resp.text()[:250]
            except Exception:
                body = ""
            print(f"[NET {resp.status}] {url} -> {body}")

    page.on("response", on_response)

    # 1. Ensure sidebar is open
    close_btn = page.locator("button[aria-label='Close']")
    if close_btn.count() == 0 or not close_btn.first.is_visible():
        print("Opening sidebar...")
        page.evaluate("""() => {
            const btn = document.querySelector("button[aria-label='Feedback']");
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(1000)
    dismiss_timer()

    # 2. Check if we need to click Next or Disagree to get to Submit task
    has_next = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next' && b.getBoundingClientRect().x > 750);
        return !!btn;
    }""")
    if has_next:
        print("Next button found, clicking Next...")
        page.mouse.click(946, 725)
        page.wait_for_timeout(1500)
        dismiss_timer()

    # 3. Verify Submit task button
    sub_btn = page.locator("button:has-text('Submit task')").first
    print("Submit task button visible:", sub_btn.is_visible())
    box = sub_btn.bounding_box()
    print("Submit task button bounding box:", box)

    # 4. CLICK SUBMIT TASK!
    print("\n==========================================")
    print(">>> CLICKING 'Submit task' BUTTON NOW! <<<")
    print("==========================================")
    if box:
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    else:
        page.evaluate("""() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
            if (btn) btn.click();
        }""")
    
    page.wait_for_timeout(1000)
    dismiss_timer()

    # 5. Monitor for modal, redirect, or success for up to 25 seconds
    submitted = False
    for sec in range(1, 26):
        page.wait_for_timeout(1000)
        
        # Check if timer paused, dismiss it
        st = page.locator("button:has-text('Start timer')").first
        if st.is_visible():
            b = st.bounding_box()
            if b:
                print(f"[{sec}s] Dismissing timer overlay...")
                page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                page.wait_for_timeout(500)

        # Check for dialogs (Confirm time, Confirm, Submit, etc.)
        dialog_text = page.evaluate("""() => {
            const d = document.querySelector('div[role=\"dialog\"], [role=\"alertdialog\"]');
            if (!d) return null;
            return d.innerText;
        }""")

        if dialog_text:
            print(f"[{sec}s] Dialog detected:\n{dialog_text[:300]}")
            # Look for confirmation buttons
            confirm_btn = page.locator("button:has-text('Confirm time'), button:has-text('Confirm'), button:has-text('Submit anyway'), button:has-text('Yes'), button:has-text('Submit')").first
            if confirm_btn.count() > 0 and confirm_btn.is_visible():
                btn_name = confirm_btn.inner_text().strip()
                if btn_name != "Submit task":
                    print(f"[{sec}s] Clicking confirmation button '{btn_name}'!")
                    confirm_btn.click()
                    page.wait_for_timeout(2000)

        # Check URL
        curr_url = page.url
        curr_title = page.title()
        if "/run" not in curr_url or "submitted" in curr_url.lower():
            print(f"[{sec}s] URL CHANGED TO: {curr_url}")
            submitted = True
            break

        # Check if page body indicates submitted or read only
        status_check = page.evaluate("""() => {
            const text = document.body.innerText;
            return {
                isReadOnly: text.includes('read only') || text.includes('Submitted') || text.includes('Under review') || text.includes('Task submitted'),
                submitBtnText: (() => {
                    const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Submit'));
                    return btn ? btn.innerText.trim() : null;
                })()
            };
        }""")
        if status_check["isReadOnly"]:
            print(f"[{sec}s] PAGE IS NOW IN SUBMITTED / READ-ONLY STATE!")
            submitted = True
            break
        elif status_check["submitBtnText"]:
            print(f"[{sec}s] Submit button state: {status_check['submitBtnText']}")

    # 6. Capture proof screenshot
    page.screenshot(path="handshake/scratch/proof_final_delivery_complete.png")
    print("\nProof screenshot saved to handshake/scratch/proof_final_delivery_complete.png")
    print("Final URL:", page.url)
    print("Final Title:", page.title())
