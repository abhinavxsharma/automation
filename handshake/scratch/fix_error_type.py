import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # 1. Locate Error Type card and click Edit this step
    print("Finding Error Type edit button...")
    clicked = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const header = all.find(el => el.innerText && el.innerText.trim() === 'Error Type' && el.children.length === 0);
        if (!header) return { error: "Header not found" };
        let p = header;
        while (p && p !== document.body) {
            const btn = p.querySelector('button[aria-label="Edit this step"]');
            if (btn) {
                btn.scrollIntoView({ behavior: 'instant', block: 'center' });
                btn.click();
                return { success: true };
            }
            p = p.parentElement;
        }
        return { error: "Edit button not found" };
    }""")
    print("Click edit result:", clicked)
    page.wait_for_timeout(1500)
    
    # Take screenshot of open edit state
    page.screenshot(path="scratch/error_type_edit_open.png")
    
    # Check what radios / options exist
    radios_info = page.evaluate("""() => {
        const radios = Array.from(document.querySelectorAll('input[type="radio"], [role="radio"]'));
        return radios.map(r => {
            const label = r.closest('label') || r.parentElement;
            return {
                checked: r.checked,
                text: label ? label.innerText.trim().slice(0, 80) : ''
            };
        });
    }""")
    print(f"Radios found: {len(radios_info)}")
    for r in radios_info:
        print(" ", r)
