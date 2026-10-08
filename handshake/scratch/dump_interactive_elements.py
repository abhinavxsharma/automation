import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    try:
        page.locator("[data-testid='task-run-skeleton']").wait_for(state="hidden", timeout=15000)
    except Exception:
        pass
    page.wait_for_timeout(3000)

    elements = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const results = [];
        for (const el of all) {
            const tag = el.tagName.toLowerCase();
            const role = el.getAttribute('role') || '';
            const txt = (el.innerText || '').trim();
            const aria = el.getAttribute('aria-label') || '';
            const testid = el.getAttribute('data-testid') || '';
            
            // Check if interactive
            if (
                tag === 'button' ||
                tag === 'a' ||
                tag === 'input' ||
                tag === 'textarea' ||
                role === 'button' ||
                role === 'tab' ||
                txt === 'Start' ||
                txt === 'Save' ||
                aria.length > 0 ||
                testid.length > 0
            ) {
                const rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    results.push({
                        tag,
                        role,
                        text: txt.substring(0, 50),
                        aria,
                        testid,
                        className: typeof el.className === 'string' ? el.className.substring(0, 50) : '',
                        rect: {
                            x: Math.round(rect.x),
                            y: Math.round(rect.y),
                            w: Math.round(rect.width),
                            h: Math.round(rect.height)
                        }
                    });
                }
            }
        }
        return results;
    }""")

    with open("scratch/interactive_elements.json", "w", encoding="utf-8") as f:
        json.dump(elements, f, indent=2)

    print(f"Found {len(elements)} interactive elements. Saved to scratch/interactive_elements.json.")
    for el in elements:
        if el["rect"]["x"] > 600 or "start" in el["text"].lower() or "save" in el["text"].lower():
            print(el)
