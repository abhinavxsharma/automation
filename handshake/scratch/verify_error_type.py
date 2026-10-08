import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(2000)
    
    # Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)
    
    # Check Error Type section
    err_text = page.evaluate("""() => {
        const headers = Array.from(document.querySelectorAll('h3, h4, div')).filter(d => d.innerText && d.innerText.includes('Error Type'));
        const h = headers.find(el => el.children.length === 0 || el.innerText.trim() === 'Error Type');
        if (h) {
            const container = h.closest('div.border, div[data-block-id], section') || h.parentElement.parentElement;
            return container.innerText;
        }
        return 'Not found';
    }""")
    print("=== ERROR TYPE SECTION ===")
    print(err_text)
    
    page.screenshot(path="scratch/error_type_verified.png")
