import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    steps = pg.evaluate('''() => {
        const editBtns = Array.from(document.querySelectorAll('button[aria-label="Edit this step"]'));
        return editBtns.map((btn, idx) => {
            let parent = btn.parentElement;
            for (let i = 0; i < 5; i++) {
                if (!parent) break;
                if (parent.innerText && parent.innerText.length > 20) break;
                parent = parent.parentElement;
            }
            const snippet = parent ? parent.innerText.slice(0, 150).replace(/\\n/g, ' ') : '';
            return { idx, snippet };
        });
    }''')
    
    print(f"Total 'Edit this step' buttons: {len(steps)}")
    with open("scratch/mapped_steps.txt", "w", encoding="utf-8") as f:
        for s in steps:
            line = f"Step {s['idx']:2d}: {s['snippet']}"
            f.write(line + "\n")
            print(f"Step {s['idx']:2d}: {s['snippet'].encode('ascii', 'replace').decode('ascii')}")
