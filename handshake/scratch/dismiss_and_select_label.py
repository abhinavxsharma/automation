import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # Check if Start timer button is visible
    st = page.locator("button:has-text('Start timer')").first
    print("Is Start timer visible now:", st.is_visible())
    if st.is_visible():
        box = st.bounding_box()
        print("Box:", box)
        page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
        print("Clicked mouse at center of Start timer!")
        page.wait_for_timeout(1500)
    
    page.screenshot(path="scratch/after_dismiss_timer_modal.png")
    
    # Now check if Label mis-binding option is visible on screen
    # It starts with "Label" and "mis-binding"
    opt = page.locator("text=/Label.*mis-binding/").first
    print("Label mis-binding option visible:", opt.is_visible())
    if opt.is_visible():
        box = opt.bounding_box()
        print("Option box:", box)
        page.mouse.click(box["x"] + 20, box["y"] + box["height"]/2)
        print("Clicked Label mis-binding option!")
        page.wait_for_timeout(1000)
        
    # Check arrow button next to Cancel
    arrow_btn = page.locator("button:has(svg.lucide-arrow-up), button:has(svg)").filter(has=page.locator("xpath=preceding-sibling::button[contains(text(), 'Cancel')]")).first
    # Or find button adjacent to Cancel
    cancel = page.locator("button:has-text('Cancel')").first
    print("Cancel visible:", cancel.is_visible())
    
    # Commit via JS
    res = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button" };
        const parent = cancelBtn.parentElement;
        const arrowBtn = Array.from(parent.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (arrowBtn) {
            arrowBtn.click();
            return { success: true };
        }
        return { error: "No arrow button" };
    }""")
    print("JS Commit arrow result:", res)
    page.wait_for_timeout(2000)
    
    page.screenshot(path="scratch/after_commit_step14.png")
