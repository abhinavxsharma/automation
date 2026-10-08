import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/live_full_reloaded_text.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Full text length: {len(text)}")
    
    # Check sections
    for header in ["Block 1 Responses:", "Block 2 Responses:", "Step-by-step solution:", "Final Answer:", "Distractor #1:", "Distractor #2:", "Science Judge:"]:
        if header in text:
            print(f"FOUND: {header}")
        else:
            print(f"NOT FOUND: {header}")
            
    # List all edit buttons and their labels/indices
    btns = pg.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll('button[aria-label="Edit this step"]'));
        return editBtns.map((b, i) => {
            let p = b;
            for (let j = 0; j < 5; j++) {
                if (p.parentElement && p.parentElement.innerText.length > p.innerText.length + 20) {
                    p = p.parentElement;
                } else if (p.parentElement) {
                    p = p.parentElement;
                }
            }
            return {
                idx: i,
                snippet: p ? p.innerText.slice(0, 100).replace(/\\n/g, ' ') : ''
            };
        });
    }""")
    print("\nEdit buttons count:", len(btns))
    for b in btns:
        print(f"  [{b['idx']}] {b['snippet'][:80]}")
