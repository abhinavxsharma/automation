import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    res = page.evaluate("""() => {
        // Find element containing "Write a detailed description"
        const all = Array.from(document.querySelectorAll('*'));
        const descHeader = all.find(el => el.innerText && el.innerText.includes('Write a detailed description') && el.children.length === 0);
        const sjHeader = all.find(el => el.innerText && el.innerText.includes('Pay close attention to the Science Judge') && el.children.length === 0);

        // Find nearest Edit button after descHeader
        function findEditButtonNear(targetEl) {
            if (!targetEl) return null;
            let p = targetEl;
            // Traverse up until we find a container with an edit button
            while (p && p !== document.body) {
                const btn = p.querySelector('button[aria-label="Edit this step"]');
                if (btn) return {
                    rect: btn.getBoundingClientRect(),
                    aria: btn.getAttribute('aria-label'),
                    parentTag: p.tagName,
                    parentClass: p.className
                };
                p = p.parentElement;
            }
            return null;
        }

        return {
            descFound: !!descHeader,
            descEdit: findEditButtonNear(descHeader),
            sjFound: !!sjHeader,
            sjEdit: findEditButtonNear(sjHeader)
        };
    }""")

    print("Result:", res)
