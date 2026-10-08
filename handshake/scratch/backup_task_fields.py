import json
import sys

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    backup_data = page.evaluate("""() => {
        const data = {};
        
        // Find all cards or steps
        const containers = Array.from(document.querySelectorAll('div')).filter(el => {
            const h = el.querySelector('h1, h2, h3, h4, [class*="title"], [class*="header"]');
            return h && h.innerText && h.innerText.trim().length > 3;
        });
        
        // Grab the full body text
        data.full_body_text = document.body.innerText;
        
        // Specific sections by searching text
        const text = document.body.innerText;
        
        return data;
    }""")

    with open(
        "handshake/scratch/backup_task_fields.json", "w", encoding="utf-8"
    ) as f:
        json.dump(backup_data, f, indent=2)

    print("Saved backup_task_fields.json")
