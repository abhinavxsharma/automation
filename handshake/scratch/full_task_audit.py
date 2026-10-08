import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(2000)

    audit_data = page.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        const getCardText = (btn) => {
            if (!btn) return 'NOT_FOUND';
            let el = btn.parentElement;
            while (el && !el.getAttribute('data-block-id') && !el.classList.contains('border') && el !== document.body) {
                el = el.parentElement;
            }
            return el ? el.innerText.trim() : 'NO_PARENT';
        };

        const getCardHTML = (btn) => {
            if (!btn) return '';
            let el = btn.parentElement;
            while (el && !el.getAttribute('data-block-id') && !el.classList.contains('border') && el !== document.body) {
                el = el.parentElement;
            }
            return el ? el.innerHTML : '';
        };

        const cards = editBtns.map((b, i) => ({
            index: i,
            text: getCardText(b),
            hasKaTeX: !!(b.parentElement && getCardHTML(b).includes('katex'))
        }));

        const sidebar = document.querySelector("[data-testid='task-side-panel'], div.w-80");

        return {
            totalEditBtns: editBtns.length,
            cards: cards,
            sidebarText: sidebar ? sidebar.innerText.trim() : ''
        };
    }""")

    print(f"Total Edit Steps Found: {audit_data['totalEditBtns']}")
    for c in audit_data['cards']:
        print(f"\n{'='*20} STEP {c['index']} (KaTeX={c['hasKaTeX']}) {'='*20}")
        print(c['text'][:300] + ("..." if len(c['text']) > 300 else ""))

    print(f"\n{'='*20} SIDEBAR STATUS {'='*20}")
    print(audit_data['sidebarText'])
