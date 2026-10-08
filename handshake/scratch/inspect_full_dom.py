import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    res = pg.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll('button[aria-label="Edit this step"]'));
        return editBtns.map((btn, idx) => {
            let container = btn;
            for (let i = 0; i < 5; i++) {
                if (!container) break;
                if (container.parentElement && container.parentElement.innerText.length > container.innerText.length + 30) {
                    container = container.parentElement;
                } else {
                    container = container.parentElement;
                }
            }
            return {
                idx,
                text: container ? container.innerText.slice(0, 300) : 'none'
            };
        });
    }""")
    for item in res:
        print(f"--- Step edit button {item['idx']} ---")
        print(item['text'].encode('ascii', 'replace').decode('ascii'))
