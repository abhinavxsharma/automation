import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # Find the badge with 'Connectivity / topology error'
    btn_info = page.evaluate("""() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        let targetEl = null;
        while (node = walker.nextNode()) {
            if (node.nodeValue && node.nodeValue.includes('Connectivity / topology error')) {
                targetEl = node.parentElement;
                break;
            }
        }
        if (!targetEl) return { error: "Badge not found" };
        
        // Find container and pencil button
        const container = targetEl.closest('div.flex-col') || targetEl.parentElement.parentElement;
        const pencil = container.querySelector('button[aria-label="Edit this step"]') || 
                       Array.from(container.querySelectorAll('button')).find(b => b.querySelector('svg'));
        
        if (pencil) {
            pencil.scrollIntoView({ behavior: 'instant', block: 'center' });
            pencil.click();
            return {
                success: true,
                pencilOuter: pencil.outerHTML
            };
        }
        return { error: "Pencil not found in container", containerHTML: container.outerHTML.slice(0, 300) };
    }""")
    print("Click pencil result:", btn_info)
    page.wait_for_timeout(2000)
    page.screenshot(path="scratch/after_pencil_error_type.png")
