import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    res = page.evaluate("""() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        let node;
        let targetEl = null;
        while (node = walker.nextNode()) {
            if (node.nodeValue && node.nodeValue.includes('Connectivity / topology error')) {
                targetEl = node.parentElement;
                break;
            }
        }
        if (!targetEl) return null;
        
        let curr = targetEl;
        const parents = [];
        while (curr && curr !== document.body) {
            const btns = Array.from(curr.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label') || '',
                html: b.outerHTML.slice(0, 100)
            }));
            parents.push({
                tag: curr.tagName,
                class: curr.className,
                buttonCount: btns.length,
                buttons: btns
            });
            curr = curr.parentElement;
        }
        return parents;
    }""")
    print("Hierarchy count:", len(res))
    for i, p in enumerate(res[:6]):
        print(f"[{i}] {p['tag']} class={p['class'][:40]}")
        for b in p['buttons']:
            print(f"     button: aria='{b['aria']}', text='{b['text']}'")
