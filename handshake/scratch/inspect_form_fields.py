import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Continue');
        if (!btn) return 'No continue button found';
        const form = btn.closest('form') || btn.parentElement;
        
        const inputs = Array.from(form.querySelectorAll('input, select, textarea')).map(inp => ({
            name: inp.name,
            type: inp.type,
            value: inp.value,
            checked: inp.checked,
            required: inp.required,
            valid: inp.checkValidity ? inp.checkValidity() : true,
            msg: inp.validationMessage
        }));
        
        return {
            formTag: form.tagName,
            inputs
        };
    }""")
    print("Form info:", info)
