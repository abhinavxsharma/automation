import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    btn = page.locator("button[aria-label='Feedback']")
    print("Feedback btn visible:", btn.is_visible())
    btn.click()
    page.wait_for_timeout(2000)
    page.screenshot(path="scratch/after_feedback_click.png")
    
    # Check if matches appeared
    matches = page.evaluate("""() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        const res = [];
        let node;
        while (node = walker.nextNode()) {
            if (node.nodeValue && (node.nodeValue.includes('Jimson') || node.nodeValue.includes('Image quality issue') || node.nodeValue.includes('Minor issue'))) {
                res.push({
                    text: node.nodeValue.trim().slice(0, 100),
                    tag: node.parentElement.tagName,
                    rect: node.parentElement.getBoundingClientRect()
                });
            }
        }
        return res;
    }""")
    print("Matches:", len(matches))
    for m in matches:
        print(m)
