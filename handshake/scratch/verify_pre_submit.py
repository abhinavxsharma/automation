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

    # 1. Check timer / dismiss modal if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        print("Dismissing Start timer modal...")
        st_btn.first.click()
        page.wait_for_timeout(1000)

    rt_btn = page.locator("button[aria-label='Resume timer']")
    if rt_btn.count() > 0 and rt_btn.first.is_visible():
        print("Clicking Resume timer...")
        rt_btn.first.click()
        page.wait_for_timeout(1000)

    # 2. Check Final Answer
    fa_info = page.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        const btn = editBtns[9];
        let card = btn.parentElement;
        while (card && !card.getAttribute('data-block-id') && !card.classList.contains('border') && card !== document.body) {
            card = card.parentElement;
        }
        return card.innerText.trim();
    }""")
    print("Final Answer Card Text:\n", fa_info)

    # 3. Check All 5 Distractors
    distractors_info = page.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        const res = [];
        for (let i = 18; i <= 22; i++) {
            const btn = editBtns[i];
            let card = btn.parentElement;
            while (card && !card.getAttribute('data-block-id') && !card.classList.contains('border') && card !== document.body) {
                card = card.parentElement;
            }
            res.push({
                num: i - 17,
                hasKaTeX: !!card.querySelector('.katex'),
                text: card.innerText.trim().replace(/\\n+/g, ' ')
            });
        }
        return res;
    }""")
    print("\nDistractors:")
    for d in distractors_info:
        print(f"  #{d['num']} (KaTeX={d['hasKaTeX']}): {d['text']}")

    # 4. Check Sidebar / QC
    sidebar_text = page.evaluate("""() => {
        const side = document.querySelector("[data-testid='task-side-panel'], div.w-80");
        return side ? side.innerText.trim().replace(/\\n+/g, ' | ') : 'NO_SIDEBAR';
    }""")
    print("\nSidebar:\n", sidebar_text)

    # 5. Check Submit button
    submit_btn = page.locator("button:has-text('Submit task')").first
    print(f"\nSubmit task button found: {submit_btn.count() > 0}, is_visible: {submit_btn.is_visible()}, is_enabled: {submit_btn.is_enabled()}")
