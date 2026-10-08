import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    info = page.evaluate("""() => {
        const radios = Array.from(document.querySelectorAll('input[type="radio"]'));
        return radios.map(r => ({
            name: r.name,
            value: r.value,
            id: r.id,
            checked: r.checked,
            label: r.labels && r.labels[0] ? r.labels[0].innerText : (r.nextElementSibling ? r.nextElementSibling.innerText : '')
        }));
    }""")
    print("All radio inputs on page:")
    for r in info:
        print(f"  name='{r['name']}' val='{r['value']}' id='{r['id']}' checked={r['checked']} label='{r['label'][:40]}'")
