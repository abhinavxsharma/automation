import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    html = pg.evaluate("""() => {
        const root = document.querySelector('form') || document.body;
        return root.innerHTML;
    }""")
    with open("scratch/step3_form.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Wrote scratch/step3_form.html")
