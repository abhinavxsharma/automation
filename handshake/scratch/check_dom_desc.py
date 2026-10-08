import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)

    desc_info = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const header = all.find(e => e.innerText && e.innerText.includes('Write a detailed description') && e.children.length === 0);
        if (!header) return { error: 'No header' };
        let p = header;
        while (p && p.parentElement && !p.className.includes('card') && !p.className.includes('border') && p !== document.body) {
            p = p.parentElement;
        }
        return {
            text: p ? p.innerText : ''
        };
    }""")

    with open("scratch/current_desc_in_dom.txt", "w", encoding="utf-8") as f:
        f.write(desc_info.get("text", ""))

    print("Saved current desc text in DOM to scratch/current_desc_in_dom.txt")
