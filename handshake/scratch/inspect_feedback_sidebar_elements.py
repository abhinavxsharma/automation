import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Cancel any open editor first so page is calm
    page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (cancelBtn) cancelBtn.click();
    }""")

    # Find the feedback sidebar container
    sidebar_info = page.evaluate("""() => {
        // Feedback heading
        const all = Array.from(document.querySelectorAll('*'));
        const fbHeader = all.find(e => e.innerText && e.innerText.trim() === 'Feedback' && e.children.length === 0);
        if (!fbHeader) return { error: "Feedback header not found" };

        let container = fbHeader;
        while (container && container.parentElement && container.clientWidth < 250) {
            container = container.parentElement;
        }

        // Find all interactive elements inside container
        const clickables = Array.from(container.querySelectorAll('button, svg, [role="button"]')).map(el => {
            const rect = el.getBoundingClientRect();
            let parentBtn = el.closest('button') || el;
            return {
                tag: el.tagName,
                parentTag: parentBtn.tagName,
                aria: el.getAttribute('aria-label') || parentBtn.getAttribute('aria-label') || '',
                text: el.innerText ? el.innerText.trim() : '',
                rect: { x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height) }
            };
        }).filter(c => c.rect.w > 0 && c.rect.h > 0);

        return {
            containerRect: container.getBoundingClientRect(),
            containerText: container.innerText,
            clickables
        };
    }""")

    print("Sidebar Container Text:\n", sidebar_info.get("containerText"))
    print("\nClickables count:", len(sidebar_info.get("clickables", [])))
    for c in sidebar_info.get("clickables", []):
        print(f"[{c['tag']}] aria='{c['aria']}' text='{c['text']}' rect={c['rect']}")

    with open("scratch/feedback_sidebar_detail.json", "w", encoding="utf-8") as f:
        json.dump(sidebar_info, f, indent=2)
