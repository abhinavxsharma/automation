import sys

sys.path.insert(0, "handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # Let's inspect the whole task-renderer container
    form_data = page.evaluate("""() => {
        const textNodes = [];
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        while (node = walker.nextNode()) {
            const val = node.nodeValue.trim();
            if (val && !['Exit', 'Save', 'Handshake AI', 'Changes saved'].includes(val)) {
                textNodes.push(val);
            }
        }
        
        // Find Distractor #1, Final Answer, etc.
        const allText = document.body.innerText;
        
        return {
            distractor1Index: allText.indexOf('Distractor #1'),
            finalAnswerIndex: allText.indexOf('Final answer'),
            imageDescIndex: allText.indexOf('Image description'),
            sampleText: allText.slice(0, 3000)
        };
    }""")
    print("Distractor #1 index:", form_data["distractor1Index"])
    print("Final answer index:", form_data["finalAnswerIndex"])
    print("Image desc index:", form_data["imageDescIndex"])
    
    # Let's search for distractor text in page
    all_text = page.locator("body").inner_text()
    for line in all_text.split("\n"):
        if any(term in line.lower() for term in ["distractor", "final answer", "science judge", "76", "85", "75"]):
            print("MATCH:", line[:120])
