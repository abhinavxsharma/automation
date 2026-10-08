import json
import sys

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    data = page.evaluate("""() => {
        const result = {
            inputs: [],
            textareas: [],
            images: [],
            blocks: []
        };
        document.querySelectorAll('input').forEach(i => {
            result.inputs.push({
                type: i.type,
                value: i.value,
                checked: i.checked,
                id: i.id,
                placeholder: i.placeholder
            });
        });
        document.querySelectorAll('textarea').forEach(t => {
            result.textareas.push({
                value: t.value,
                placeholder: t.placeholder
            });
        });
        document.querySelectorAll('img').forEach(img => {
            result.images.push({
                src: img.src.substring(0, 150),
                alt: img.alt,
                w: img.naturalWidth,
                h: img.naturalHeight
            });
        });
        // Gather text of major sections / cards
        document.querySelectorAll('[data-testid], [class*="card"], [class*="step"], [class*="block"]').forEach(el => {
            const txt = el.innerText ? el.innerText.trim() : "";
            if (txt.length > 20 && txt.length < 500) {
                result.blocks.push({
                    tag: el.tagName,
                    className: el.className,
                    text: txt.substring(0, 200)
                });
            }
        });
        return result;
    }""")

    with open("handshake/scratch/live_form_dump.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("Textareas count:", len(data["textareas"]))
    for i, t in enumerate(data["textareas"]):
        print(f"Textarea {i}: placeholder={t['placeholder']!r}, len={len(t['value'])}")
        print("  Preview:", t["value"][:100].replace("\n", " "))

    print("\nInputs with values:")
    for inp in data["inputs"]:
        if inp["value"]:
            print(f"Input ({inp['type']}): {inp['value']}")

    print("\nImages:")
    for img in data["images"]:
        print(f"Img w={img['w']} h={img['h']} src={img['src'][:60]}")
