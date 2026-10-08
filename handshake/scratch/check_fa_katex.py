import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(2000)

    # Inspect Final Answer HTML
    info = page.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        const faBtn = editBtns[9];
        if (!faBtn) return { error: 'faBtn not found', count: editBtns.length };
        let card = faBtn.parentElement;
        while (card && !card.getAttribute('data-block-id') && !card.classList.contains('border') && card !== document.body) {
            card = card.parentElement;
        }
        return {
            hasKaTeX: !!card.querySelector('.katex'),
            html: card.innerHTML,
            text: card.innerText
        };
    }""")
    print("Final answer has KaTeX:", info["hasKaTeX"])
    print("Final answer HTML snippet:\n", info["html"])
