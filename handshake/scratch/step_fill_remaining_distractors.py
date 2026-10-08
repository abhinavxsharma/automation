import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

DISTRACTORS = [
    ("Distractor #2", "89"),
    ("Distractor #3", "72"),
    ("Distractor #4", "68"),
    ("Distractor #5", "64"),
]

with sync_playwright() as p:
    ctx, pg = get_page(p)
    
    for name, val in DISTRACTORS:
        print(f"\n--- Filling {name} with '{val}' ---")
        ta = pg.locator("textarea[placeholder='Plausible-but-wrong answer text']").first
        if not ta.is_visible():
            print(f"Textarea for {name} not visible, waiting...")
            time.sleep(1)
            
        ta.fill(val, force=True)
        time.sleep(0.5)
        
        pg.evaluate(f"""(v) => {{
            const el = document.querySelector("textarea[placeholder='Plausible-but-wrong answer text']");
            if (el) {{
                el.value = v;
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}""", val)
        time.sleep(0.5)
        
        cont_btn = pg.locator("button:has-text('Continue')").first
        print("Clicking Continue...")
        cont_btn.click(force=True)
        time.sleep(2.5)
        
    pg.screenshot(path="scratch/after_all_distractors.png")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/page_after_all_distractors.txt", "w", encoding="utf-8") as f:
        f.write(text)
        
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Last 35 lines of page text ---")
    for ln in lines[-35:]:
        print(" ", ln.encode('ascii', 'replace').decode('ascii'))
