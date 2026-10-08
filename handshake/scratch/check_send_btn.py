import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button", timeout=10000)
    
    # 1. Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)
    
    # Check elements near textarea
    info = page.evaluate("""() => {
        const ta = document.querySelector('textarea, [placeholder*=\"resolve reason\"], [placeholder*=\"reply\"]');
        if (!ta) return 'No textarea';
        // Go up to the container
        const form = ta.closest('form') || ta.parentElement.parentElement;
        const all = Array.from(form.querySelectorAll('*'));
        return all.map(el => ({
            tag: el.tagName,
            cls: el.className,
            text: el.innerText ? el.innerText.slice(0, 30) : '',
            rect: el.getBoundingClientRect(),
            hasSvg: !!el.querySelector('svg')
        })).filter(x => ['BUTTON', 'SVG', 'PATH', 'FORM'].includes(x.tag) || x.hasSvg);
    }""")
    print("Elements in resolve form:")
    for item in info:
        print(item)
