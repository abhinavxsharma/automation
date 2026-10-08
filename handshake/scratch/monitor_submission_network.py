import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Listen to console and network
    page.on("console", lambda msg: print(f"[CONSOLE {msg.type}] {msg.text}"))
    page.on("pageerror", lambda err: print(f"[PAGEERROR] {err}"))
    
    def log_response(resp):
        if "joinhandshake.com" in resp.url and any(k in resp.url for k in ["task", "submit", "annotation", "graphql", "api"]):
            try:
                body = resp.text()[:200]
            except Exception:
                body = ""
            print(f"[NET {resp.status}] {resp.url} -> {body}")

    page.on("response", log_response)

    # 1. Dismiss timer
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        b = st.bounding_box()
        if b:
            page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Open sidebar if not open
    close_btn = page.locator("button[aria-label='Close']")
    if close_btn.count() == 0 or not close_btn.first.is_visible():
        print("Opening feedback sidebar...")
        page.evaluate("""() => {
            const btn = document.querySelector("button[aria-label='Feedback']");
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(1500)

    # 3. Check what button is at the bottom
    btn_info = page.evaluate("""() => {
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next' && b.getBoundingClientRect().x > 750);
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task' && b.getBoundingClientRect().x > 750);
        const disagreeBtn = document.querySelector("button[aria-label='Disagree']");
        
        return {
            hasNext: !!nextBtn,
            hasSubmit: !!submitBtn,
            hasDisagree: !!disagreeBtn,
            submitDisabled: submitBtn ? submitBtn.disabled : null,
            submitAriaDisabled: submitBtn ? submitBtn.getAttribute('aria-disabled') : null
        };
    }""")
    print("Sidebar buttons before action:", btn_info)

    # If Disagree button exists, click it
    if btn_info["hasDisagree"]:
        print("Clicking Disagree button...")
        page.evaluate("""() => {
            const btn = document.querySelector("button[aria-label='Disagree']");
            if (btn) btn.click();
        }""")
        page.wait_for_timeout(2000)

    # If Next button exists, click Next
    has_next = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next' && b.getBoundingClientRect().x > 750);
        if (btn) {
            btn.click();
            return true;
        }
        return false;
    }""")
    if has_next:
        print("Clicked Next button...")
        page.wait_for_timeout(2000)

    # 4. Now click Submit task and watch network!
    print("\n>>> Attempting to click Submit task and monitoring network responses... <<<")
    submit_clicked = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task' && b.getBoundingClientRect().x > 750);
        if (btn) {
            btn.click();
            return true;
        }
        return false;
    }""")
    print("Submit task clicked:", submit_clicked)

    # Wait up to 10 seconds and log all responses
    for i in range(10):
        page.wait_for_timeout(1000)
        # Check if confirmation dialog popped up
        has_dialog = page.evaluate("""() => {
            const d = document.querySelector('div[role=\"dialog\"], [role=\"alertdialog\"]');
            return d ? d.innerText : null;
        }""")
        if has_dialog:
            print(f"[{i}s] Dialog detected:\n", has_dialog)
            # Try to confirm
            confirm_btn = page.locator("button:has-text('Confirm time'), button:has-text('Confirm'), button:has-text('Submit anyway'), button:has-text('Yes')").first
            if confirm_btn.count() > 0 and confirm_btn.is_visible():
                print("Clicking confirmation button:", confirm_btn.inner_text().strip())
                confirm_btn.click()
                page.wait_for_timeout(3000)
                break

    page.screenshot(path="handshake/scratch/network_monitor_result.png")
    print("\nScreenshot saved to handshake/scratch/network_monitor_result.png")
    print("Final URL:", page.url)
