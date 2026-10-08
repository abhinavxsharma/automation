import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # 1. Dismiss timer modal if visible
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing timer modal...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Check if sidebar is currently open
    # We can check if any element with text 'Needs attention' exists on the right
    is_open = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('*')).filter(el => {
            const r = el.getBoundingClientRect();
            return r.x > 700 && el.innerText && el.innerText.includes('Needs attention');
        });
        return els.length > 0;
    }""")
    print("Is sidebar open:", is_open)

    if not is_open:
        print("Opening sidebar...")
        fb_btn = page.locator("button[aria-label='Feedback']")
        if fb_btn.count() > 0:
            fb_btn.first.click()
            page.wait_for_timeout(1500)

    # Re-check dismiss modal
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 3. Read sidebar details in Needs attention
    info_needs = page.evaluate("""() => {
        const rightEls = Array.from(document.querySelectorAll('*')).filter(el => {
            const r = el.getBoundingClientRect();
            return r.x > 700 && r.width > 200 && r.height > 500;
        });
        return rightEls[0] ? rightEls[0].innerText : "Not found";
    }""")
    print("=== NEEDS ATTENTION TAB TEXT ===")
    print(info_needs)

    # 4. Click "All" tab in sidebar
    clicked_all = page.evaluate("""() => {
        const allBtn = Array.from(document.querySelectorAll('*')).find(el => {
            const r = el.getBoundingClientRect();
            return r.x > 700 && el.innerText && el.innerText.trim() === 'All';
        });
        if (allBtn) {
            allBtn.click();
            return true;
        }
        return false;
    }""")
    print("Clicked All tab:", clicked_all)
    page.wait_for_timeout(1500)

    # 5. Read sidebar details in All tab
    info_all = page.evaluate("""() => {
        const rightEls = Array.from(document.querySelectorAll('*')).filter(el => {
            const r = el.getBoundingClientRect();
            return r.x > 700 && r.width > 200 && r.height > 500;
        });
        return rightEls[0] ? rightEls[0].innerText : "Not found";
    }""")
    print("=== ALL TAB TEXT ===")
    print(info_all)

    # 6. Check Submit task button
    submit_info = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        if (!btn) return null;
        return {
            text: btn.innerText,
            disabled: btn.disabled,
            ariaDisabled: btn.getAttribute('aria-disabled'),
            classes: btn.className,
            rect: btn.getBoundingClientRect()
        };
    }""")
    print("\n=== SUBMIT TASK BUTTON ===")
    print(submit_info)

    page.screenshot(path="handshake/scratch/feedback_tabs_checked.png")
    print("Screenshot saved to handshake/scratch/feedback_tabs_checked.png")
