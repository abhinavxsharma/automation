import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Step 1: Dismiss Start timer if visible
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing Start timer at", box)
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # Step 2: Locate the commit button in the Distractor #1 editor
    # In the screenshot, there is a 'Cancel' button, and right next to it is a button with an up arrow (svg)
    commit_res = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button found" };
        
        // The commit button is in the same parent container as Cancel
        const parent = cancelBtn.parentElement;
        const siblingBtns = Array.from(parent.querySelectorAll('button')).filter(b => b !== cancelBtn);
        if (siblingBtns.length > 0) {
            const commitBtn = siblingBtns[0];
            const rect = commitBtn.getBoundingClientRect();
            return {
                found: true,
                rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height },
                html: commitBtn.outerHTML
            };
        }
        return { error: "No sibling commit button found" };
    }""")
    print("Commit button search:", commit_res)

    if commit_res.get("found"):
        rect = commit_res["rect"]
        print(f"Clicking commit button at ({rect['x'] + rect['width']/2}, {rect['y'] + rect['height']/2})...")
        page.mouse.click(rect["x"] + rect["width"] / 2, rect["y"] + rect["height"] / 2)
        page.wait_for_timeout(1500)

    # Step 3: Click top Save button
    save_btn = page.locator("button:has-text('Save')").first
    if save_btn.is_visible():
        print("Clicking top Save button...")
        save_btn.click()
        page.wait_for_timeout(2000)

    # Step 4: Inspect the Science Judge card and its circle-slash button, plus the Next button
    sidebar_info = page.evaluate("""() => {
        const sjCard = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.includes('Science Judge - Lumiere') && e.children.length > 1);
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next' || b.innerText.trim() === 'Submit task');
        
        let sjBtns = [];
        if (sjCard) {
            sjBtns = Array.from(sjCard.querySelectorAll('button')).map(b => ({
                aria: b.getAttribute('aria-label'),
                rect: b.getBoundingClientRect(),
                html: b.outerHTML.substring(0, 100)
            }));
        }

        const addressed = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/));

        return {
            hasSjCard: !!sjCard,
            sjBtns: sjBtns,
            nextBtn: nextBtn ? {
                text: nextBtn.innerText.trim(),
                rect: nextBtn.getBoundingClientRect(),
                disabled: nextBtn.disabled
            } : null,
            addressedText: addressed ? addressed.innerText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/)[0] : null
        };
    }""")
    print("Sidebar state after commit & save:\n", sidebar_info)

    page.screenshot(path="scratch/after_commit_and_inspect.png")
    print("Saved scratch/after_commit_and_inspect.png")
