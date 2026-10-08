import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # Find the edit button for description
    found = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const descHeader = all.find(el => el.innerText && el.innerText.includes('Write a detailed description') && el.children.length === 0);
        if (!descHeader) return null;
        let p = descHeader;
        while (p && p !== document.body) {
            const btn = p.querySelector('button[aria-label="Edit this step"]');
            if (btn) {
                btn.scrollIntoView({ behavior: 'instant', block: 'center' });
                return true;
            }
            p = p.parentElement;
        }
        return false;
    }""")

    print("Scrolled to descHeader:", found)
    page.wait_for_timeout(500)
    page.screenshot(path="scratch/before_desc_edit.png")

    # Now click the edit button
    clicked = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const descHeader = all.find(el => el.innerText && el.innerText.includes('Write a detailed description') && el.children.length === 0);
        if (!descHeader) return null;
        let p = descHeader;
        while (p && p !== document.body) {
            const btn = p.querySelector('button[aria-label="Edit this step"]');
            if (btn) {
                btn.click();
                return true;
            }
            p = p.parentElement;
        }
        return false;
    }""")
    print("Clicked desc edit button:", clicked)
    page.wait_for_timeout(1500)
    page.screenshot(path="scratch/after_desc_edit_open.png")

    # Inspect what opened
    opened_info = page.evaluate("""() => {
        const textareas = Array.from(document.querySelectorAll('textarea')).map(t => ({
            value: t.value.substring(0, 80),
            visible: t.offsetParent !== null,
            rect: t.getBoundingClientRect()
        }));
        const buttons = Array.from(document.querySelectorAll('button')).filter(b => b.offsetParent !== null).map(b => b.innerText.trim());
        return {
            textareas,
            visibleButtons: buttons
        };
    }""")
    print("Opened info:", opened_info)
