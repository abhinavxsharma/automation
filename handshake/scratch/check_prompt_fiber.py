import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_timeout(2000)
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # Let's inspect the Prompt card component state
    info = page.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        const btn = editBtns[7];
        let card = btn.parentElement;
        while (card && !card.getAttribute('data-block-id') && !card.classList.contains('border') && card !== document.body) {
            card = card.parentElement;
        }
        
        function getFiber(dom) {
            const key = Object.keys(dom || {}).find(k => k.startsWith('__reactFiber$'));
            return key ? dom[key] : null;
        }
        
        const fiber = getFiber(card);
        let curr = fiber;
        let blockData = null;
        while (curr) {
            if (curr.memoizedProps && (curr.memoizedProps.block || curr.memoizedProps.task)) {
                blockData = {
                    block: curr.memoizedProps.block ? {
                        id: curr.memoizedProps.block.id,
                        type: curr.memoizedProps.block.type,
                        name: curr.memoizedProps.block.name
                    } : null
                };
                break;
            }
            curr = curr.return;
        }

        return {
            blockData: blockData
        };
    }""")
    print("Block data:", info)
