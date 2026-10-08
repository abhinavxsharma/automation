import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const toast = Array.from(document.querySelectorAll('*')).find(el => el.innerText && el.innerText.includes('This field is required'));
        if (!toast) return 'No toast found';
        
        // Find closest parent / container of toast
        return {
            tag: toast.tagName,
            text: toast.innerText,
            className: toast.className,
            rect: toast.getBoundingClientRect(),
            parentHTML: toast.parentElement ? toast.parentElement.outerHTML.slice(0, 300) : ''
        };
    }""")
    print("Toast info:", info)
