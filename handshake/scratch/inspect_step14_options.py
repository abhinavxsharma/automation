import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # 1. Dismiss timer modal
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const st = btns.find(b => b.innerText && b.innerText.includes('Start timer'));
        if (st) st.click();
    }""")
    page.wait_for_timeout(1000)
    
    # 2. Click Edit Step 14
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button[aria-label=\"Edit this step\"]'));
        const target = btns[14];
        if (target) {
            target.scrollIntoView({ behavior: 'instant', block: 'center' });
            target.click();
        }
    }""")
    page.wait_for_timeout(1500)
    
    # 3. Inspect all elements inside the active editor
    info = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button" };
        
        // Find the form container
        let container = cancelBtn;
        while (container && container.parentElement && !container.innerText.includes('Error Type')) {
            container = container.parentElement;
        }
        
        // Find all radio / option elements
        const radios = Array.from(container.querySelectorAll('[role=\"radio\"], input[type=\"radio\"], [data-state], li, label'));
        return {
            totalRadios: radios.length,
            items: radios.map(r => ({
                tag: r.tagName,
                role: r.getAttribute('role') || '',
                dataState: r.getAttribute('data-state') || '',
                ariaChecked: r.getAttribute('aria-checked') || '',
                text: r.innerText ? r.innerText.slice(0, 60).replace(/\\n/g, ' ') : ''
            })).filter(x => x.text)
        };
    }""")
    print("Found options in editor:")
    for item in info.get("items", []):
        print(item)
