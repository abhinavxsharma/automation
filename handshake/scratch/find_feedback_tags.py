import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    res = page.evaluate("""() => {
        const findEls = (selector) => {
            const out = [];
            document.querySelectorAll('*').forEach(el => {
                if (el.innerText && (el.innerText.includes('Image quality issue') || el.innerText.includes('Minor issue'))) {
                    // check if direct text
                    const hasDirect = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim().length > 0);
                    if (hasDirect) {
                        out.push({
                            tag: el.tagName,
                            cls: el.className,
                            text: el.innerText.slice(0, 100)
                        });
                    }
                }
            });
            return out;
        };
        return findEls();
    }""")
    print("Found direct text elements:", len(res))
    for r in res:
        print(r)
