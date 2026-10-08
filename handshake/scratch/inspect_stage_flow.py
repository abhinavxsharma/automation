import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Let's see what main cards / blocks are visible
    blocks = page.evaluate("""() => {
        // Collect all block titles / step titles
        const headers = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, label')).map(h => ({
            tag: h.tagName,
            text: h.innerText.trim(),
            rect: h.getBoundingClientRect()
        })).filter(h => h.text && h.rect.width > 0);
        return headers;
    }""")
    print(f"Total headers visible: {len(blocks)}")
    for h in blocks:
        print(f"  {h['tag']} (y={int(h['rect']['y'])}): {h['text'][:80]}")

    # Check for text inputs, textareas, radio buttons, etc.
    inputs = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('input, textarea, select')).map(el => ({
            tag: el.tagName,
            type: el.type,
            name: el.name,
            value: el.value ? el.value.slice(0, 50) : '',
            disabled: el.disabled,
            visible: el.getBoundingClientRect().width > 0
        })).filter(el => el.visible);
    }""")
    print(f"\nVisible inputs: {len(inputs)}")
    for inp in inputs:
        print(f"  {inp}")
