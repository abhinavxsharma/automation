import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

PAGES = [
    ("ground-rules", "https://project-lumiere-instructins.learn.joinhandshake.com/d/engineering-cs/ground-rules"),
    ("tasking-pipeline", "https://project-lumiere-instructins.learn.joinhandshake.com/d/engineering-cs/tasking-pipeline"),
    ("research-design", "https://project-lumiere-instructins.learn.joinhandshake.com/d/engineering-cs/research-design"),
    ("submission-checklist", "https://project-lumiere-instructins.learn.joinhandshake.com/d/engineering-cs/research-design/submission-checklist"),
    ("images-to-use", "https://project-lumiere-instructins.learn.joinhandshake.com/d/engineering-cs/research-design/images-to-use"),
    ("writing-prompts", "https://project-lumiere-instructins.learn.joinhandshake.com/d/engineering-cs/research-design/writing-prompts"),
    ("common-pitfalls", "https://project-lumiere-instructins.learn.joinhandshake.com/d/engineering-cs/research-design/common-pitfalls"),
    ("golden-examples", "https://project-lumiere-instructins.learn.joinhandshake.com/d/engineering-cs/research-design/golden-examples"),
    ("reviewing", "https://project-lumiere-instructins.learn.joinhandshake.com/d/engineering-cs/research-design/reviewing"),
    ("faqs", "https://project-lumiere-instructins.learn.joinhandshake.com/d/engineering-cs/faqs"),
]

with sync_playwright() as p:
    ctx, _ = get_page(p)
    page = ctx.new_page()
    
    all_hits = []
    
    for name, url in PAGES:
        try:
            page.goto(url, timeout=20000)
            time.sleep(2)
            page.evaluate('''() => {
                const backdrops = document.querySelectorAll('div.fixed.inset-0, [role="dialog"]');
                for (const b of backdrops) b.remove();
            }''')
            body = page.evaluate("() => document.body ? document.body.innerText : ''")
            with open(f"scratch/guide_{name}.txt", "w", encoding="utf-8") as f:
                f.write(body)
                
            for line in body.splitlines():
                l = line.lower()
                if "pass @" in l or "holding" in l or "pass@" in l or "pass rate" in l:
                    all_hits.append(f"[{name}] {line.strip()}")
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            
    print(f"\nTotal targeted hits: {len(all_hits)}")
    for h in all_hits[:30]:
        print(" ", h.encode('ascii', 'replace').decode('ascii'))
