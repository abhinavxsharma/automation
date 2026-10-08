import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # Click Edit on Step 7
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    edit_btns[7].scroll_into_view_if_needed()
    time.sleep(0.5)
    edit_btns[7].click(force=True)
    time.sleep(2)
    
    # Inspect the thumbnail area
    thumb_info = pg.evaluate("""() => {
        const imgs = Array.from(document.querySelectorAll('div.relative img, div.group img, div:has(> img)'));
        return imgs.map(el => {
            const container = el.closest('div.relative, div.group') || el.parentElement;
            return {
                imgSrc: el.src ? el.src.slice(0, 100) : '',
                containerHTML: container ? container.outerHTML.slice(0, 300) : '',
                buttonsInContainer: container ? Array.from(container.querySelectorAll('button')).map(b => ({
                    aria: b.getAttribute('aria-label'),
                    title: b.getAttribute('title'),
                    className: b.className,
                    svg: b.querySelector('svg')?.outerHTML?.slice(0, 100)
                })) : []
            };
        });
    }""")
    print("Thumbnail containers info:", thumb_info)
    
    # Also find input[type=file]
    files = pg.evaluate("""() => {
        return Array.from(document.querySelectorAll('input[type="file"]')).map(inp => ({
            id: inp.id,
            name: inp.name,
            files: Array.from(inp.files).map(f => f.name)
        }));
    }""")
    print("File inputs:", files)
