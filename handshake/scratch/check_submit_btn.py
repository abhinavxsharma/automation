import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button", timeout=10000)
    
    # 1. Dismiss timer modal if present
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(500)
    
    # Check Submit task button
    info = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button')).filter(b => b.innerText && b.innerText.includes('Submit'));
        return btns.map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            disabled: b.disabled,
            ariaDisabled: b.getAttribute('aria-disabled'),
            cls: b.className,
            rect: b.getBoundingClientRect()
        }));
    }""")
    print("Submit buttons:", info)
