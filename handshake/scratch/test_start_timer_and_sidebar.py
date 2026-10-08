import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    
    # Click Start timer button
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0:
        box = st_btn.first.bounding_box()
        print("Clicking Start timer at", box)
        page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        page.wait_for_timeout(1000)

    # Check sidebar class
    sidebar_class = page.evaluate("""() => {
        const h3 = Array.from(document.querySelectorAll('h3')).find(e => e.innerText.trim() === 'Feedback');
        let curr = h3;
        while (curr && !curr.className.includes('bg-rosetta-bg-surface')) curr = curr.parentElement;
        return curr ? curr.className : 'Not found';
    }""")
    print("Sidebar class after Start timer:", sidebar_class)

    # Check buttons inside sidebar now
    buttons_in_sidebar = page.evaluate("""() => {
        const h3 = Array.from(document.querySelectorAll('h3')).find(e => e.innerText.trim() === 'Feedback');
        let curr = h3;
        while (curr && !curr.className.includes('bg-rosetta-bg-surface')) curr = curr.parentElement;
        if (!curr) return [];
        return Array.from(curr.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            disabled: b.disabled,
            rect: b.getBoundingClientRect()
        }));
    }""")
    print("Buttons in sidebar:", buttons_in_sidebar)
    page.screenshot(path="scratch/after_start_timer_clicked.png")
