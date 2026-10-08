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

    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        st_btn.first.click()
        page.wait_for_timeout(1000)

    # Inspect all distractor cards HTML and KaTeX
    info = page.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        // Distractors are buttons 18, 19, 20, 21, 22
        const res = [];
        for (let i = 18; i <= 22; i++) {
            const btn = editBtns[i];
            if (!btn) continue;
            let card = btn.parentElement;
            while (card && !card.getAttribute('data-block-id') && !card.classList.contains('border') && card !== document.body) {
                card = card.parentElement;
            }
            res.push({
                distractorNum: i - 17,
                hasKaTeX: !!card.querySelector('.katex'),
                html: card.innerHTML,
                text: card.innerText
            });
        }
        return res;
    }""")

    for r in info:
        print(f"=== Distractor {r['distractorNum']} ===")
        print(f"Has KaTeX: {r['hasKaTeX']}")
        print(f"Text:\n{r['text']}")
        print(f"HTML snippet:\n{r['html'][:300]}\n")
