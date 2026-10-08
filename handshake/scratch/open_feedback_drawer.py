import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    
    # 1. Dismiss timer modal if present
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(500)
    
    # 2. Find and click the feedback/checklist icon in the top header
    # Let's inspect buttons in the top 60px
    res = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button')).filter(b => {
            const r = b.getBoundingClientRect();
            return r.top >= 0 && r.bottom <= 60 && r.right > 800;
        });
        return btns.map((b, i) => ({
            i,
            text: b.innerText,
            aria: b.getAttribute('aria-label'),
            title: b.getAttribute('title'),
            cls: b.className,
            rect: b.getBoundingClientRect(),
            html: b.innerHTML.slice(0, 150)
        }));
    }""")
    print("Top right buttons:", res)
    
    # The checklist button is typically the one with list/check SVG
    clicked = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button')).filter(b => {
            const r = b.getBoundingClientRect();
            return r.top >= 0 && r.bottom <= 60 && r.right > 800;
        });
        // Find the button with checklist icon (usually contains path with checkmarks or list)
        // In the top bar: Save is text, then T (type/font), then checklist icon
        const checkBtn = btns.find(b => b.innerHTML.includes('<svg') && !b.innerText.includes('Save') && !b.innerText.includes('Exit'));
        if (checkBtn) {
            checkBtn.click();
            return { clicked: true, html: checkBtn.innerHTML.slice(0, 100) };
        }
        return { clicked: false };
    }""")
    print("Clicked button:", clicked)
    page.wait_for_timeout(1500)
    
    page.screenshot(path="scratch/after_checklist_toggle.png")
