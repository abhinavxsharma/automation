import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(2000)
    
    # Locate the element whose text is exactly 'Connectivity / topology error'
    # And find the pencil icon next to it
    res = page.evaluate("""() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        let badge = null;
        while (node = walker.nextNode()) {
            if (node.nodeValue && node.nodeValue.trim() === 'Connectivity / topology error') {
                badge = node.parentElement;
                break;
            }
        }
        if (!badge) return { error: "Badge not found" };
        
        // Find the container holding the badge and the edit pencil
        // In the screenshot, the pencil is right next to or below the badge
        let curr = badge.parentElement;
        for (let i = 0; i < 5; i++) {
            if (!curr) break;
            const pencil = curr.querySelector('button[aria-label=\"Edit this step\"], button:has(svg)');
            if (pencil) {
                pencil.scrollIntoView({ behavior: 'instant', block: 'center' });
                pencil.click();
                return { success: true, pencilTag: pencil.tagName, pencilAria: pencil.getAttribute('aria-label') };
            }
            curr = curr.parentElement;
        }
        return { error: "No pencil found near badge" };
    }""")
    print("Click pencil result:", res)
    page.wait_for_timeout(2000)
    page.screenshot(path="scratch/after_pencil_error_type.png")
