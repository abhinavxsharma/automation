import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    # 1. Dismiss modal first
    print("Dismissing modal...")
    dismissed = page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Start timer'));
        if (btn) btn.click();
        const overlays = Array.from(document.querySelectorAll('div[class*="z-50"]'));
        overlays.forEach(o => o.remove());
        return 'Done modal clearing';
    }""")
    print(dismissed)
    page.wait_for_timeout(1000)

    # 2. Click the up arrow button next to Cancel
    click_res = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button" };
        const parent = cancelBtn.parentElement;
        const arrowBtn = Array.from(parent.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (arrowBtn) {
            arrowBtn.click();
            return { success: true };
        }
        return { error: "No arrow button" };
    }""")
    print("Clicked commit arrow:", click_res)
    page.wait_for_timeout(2000)

    # 3. Click top Save
    save_res = page.evaluate("""() => {
        const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (saveBtn) {
            saveBtn.click();
            return 'Clicked Save';
        }
        return 'No Save button';
    }""")
    print("Top save:", save_res)
    page.wait_for_timeout(3000)

    # 4. Check if Science Judge section now displays the text!
    display_info = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const target = all.find(e => e.innerText && e.innerText.includes('Pay close attention to the Science Judge') && e.children.length === 0);
        let c = target;
        for (let i = 0; i < 5; i++) if (c && c.parentElement) c = c.parentElement;
        return {
            text: c ? c.innerText : 'Not found',
            hasJustification: c ? c.innerText.includes('automated false positive') : false
        };
    }""")
    print("Display info:", display_info)

    page.screenshot(path="scratch/sj_committed_result.png")
    print("Saved screenshot to scratch/sj_committed_result.png")
