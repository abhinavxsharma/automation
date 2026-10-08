import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    # Click the paper airplane button
    res = pg.evaluate('''() => {
        const ta = document.querySelector('textarea[placeholder*="resolve reason"]');
        if (!ta) return { error: "No resolve textarea" };
        let parent = ta.parentElement;
        let planeBtn = null;
        for (let i = 0; i < 4; i++) {
            if (!parent) break;
            const btns = Array.from(parent.querySelectorAll('button'));
            planeBtn = btns.find(b => b.querySelector('svg') && !b.innerText.includes('Cancel'));
            if (planeBtn) break;
            parent = parent.parentElement;
        }
        if (planeBtn) {
            planeBtn.scrollIntoView({ behavior: 'instant', block: 'center' });
            planeBtn.click();
            return { success: true, btnHtml: planeBtn.outerHTML };
        }
        return { error: "No plane button found" };
    }''')
    print("Click paper airplane:", res)
    time.sleep(2)
    
    pg.screenshot(path="scratch/after_plane_click.png")
    cnt = pg.evaluate('''() => {
        const m = document.body.innerText.match(/\\d+ \\/ \\d+ items addressed/);
        return m ? m[0] : 'Not found';
    }''')
    print("Counter now:", cnt)
