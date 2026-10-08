import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    btn14 = page.locator("button[aria-label='Edit this step']").nth(14)
    btn14.scroll_into_view_if_needed()
    btn14.click()
    page.wait_for_timeout(1500)
    
    page.screenshot(path="scratch/after_click_edit_14.png")
    
    radios_info = page.evaluate("""() => {
        const radios = Array.from(document.querySelectorAll('input[type="radio"], [role="radio"]'));
        return radios.map(r => {
            const label = r.closest('label') || r.parentElement;
            return {
                id: r.id,
                value: r.value,
                checked: r.checked,
                text: label ? label.innerText.trim().slice(0, 100) : ''
            };
        });
    }""")
    print(f"Radios found: {len(radios_info)}")
    for r in radios_info:
        print(" ", r)
