import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    cards_text = page.evaluate("""() => {
        // Find the feedback container
        const items = Array.from(document.querySelectorAll('*'))
            .filter(e => e.innerText && e.innerText.includes('Jimson'));
        // Find smallest elements containing full cards
        return items.map(el => ({
            tag: el.tagName,
            className: el.className,
            text: el.innerText
        }));
    }""")
    
    # Write to file
    out = []
    for c in cards_text:
        out.append(f"TAG: {c['tag']}\nCLASS: {c['className']}\nTEXT:\n{c['text']}\n" + "="*50)
    
    Path("scratch/jimson_cards_detailed.txt").write_text("\n\n".join(out), encoding="utf-8")
    print("Saved to scratch/jimson_cards_detailed.txt")
