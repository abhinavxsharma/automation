import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("[data-feedback-item-id='a98b7003-0d11-45a9-9af2-8d73fca4b800']", timeout=10000)
    
    # 1. Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)
    
    # Click Resolve on a98b7003
    page.evaluate("""() => {
        const item = document.querySelector('[data-feedback-item-id=\"a98b7003-0d11-45a9-9af2-8d73fca4b800\"]');
        const btn = item.querySelector('button[aria-label=\"Resolve\"]');
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1500)
    
    # Check elements inside item now
    elements = page.evaluate("""() => {
        const item = document.querySelector('[data-feedback-item-id=\"a98b7003-0d11-45a9-9af2-8d73fca4b800\"]');
        const inputs = Array.from(item.querySelectorAll('input, textarea, [contenteditable=\"true\"], [placeholder]'));
        const buttons = Array.from(item.querySelectorAll('button'));
        return {
            inputs: inputs.map(i => ({
                tag: i.tagName,
                type: i.type,
                placeholder: i.placeholder || i.getAttribute('placeholder'),
                cls: i.className
            })),
            buttons: buttons.map(b => ({
                aria: b.getAttribute('aria-label'),
                text: b.innerText,
                disabled: b.disabled,
                svg: b.querySelector('svg')?.outerHTML.slice(0, 60)
            }))
        };
    }""")
    print("Inputs:", elements["inputs"])
    print("Buttons:", elements["buttons"])
