import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    info = pg.evaluate("""() => {
        const ta = document.querySelector('textarea, [contenteditable="true"]');
        if (!ta) return { found: false };
        return {
            found: true,
            tag: ta.tagName,
            val: ta.value || ta.innerText || '',
            len: (ta.value || ta.innerText || '').length
        };
    }""")
    print("Textarea info:", info)
