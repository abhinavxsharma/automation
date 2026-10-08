import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

DASHBOARD_URL = "https://ai.joinhandshake.com/fellow/15f2e875-62ac-492c-9e96-d5569635671a/tasks"

with sync_playwright() as p:
    ctx, pg = get_page(p)
    pg.goto(DASHBOARD_URL, timeout=30000)
    time.sleep(3)
    
    pg.screenshot(path="scratch/dashboard_tasks_check.png")
    print("Screenshot saved to scratch/dashboard_tasks_check.png")
    
    info = pg.evaluate('''() => {
        const rows = Array.from(document.querySelectorAll('tr, div[class*="task"], div[class*="row"], div[class*="Card"]'))
            .filter(r => r.innerText.includes('1520c') || r.innerText.includes('Lumi') || r.innerText.includes('Review'))
            .map(r => r.innerText.replace(/\\n/g, ' -- '));
        return {
            url: window.location.href,
            title: document.title,
            rows: rows.slice(0, 10),
            bodySnippet: document.body.innerText.slice(0, 1500)
        };
    }''')
    print("Dashboard URL:", info["url"])
    print("Dashboard Title:", info["title"])
    print("Found rows count:", len(info["rows"]))
    for r in info["rows"]:
        print("  ", r[:150].encode('ascii', 'replace').decode('ascii'))
