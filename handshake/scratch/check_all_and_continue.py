import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright


def dismiss_timer(page):
    st = page.locator('button:has-text("Start timer")').first
    if st.is_visible():
        box = st.bounding_box()
        if box:
            print("Dismissing Start timer modal...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            time.sleep(0.5)


with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)
    dismiss_timer(pg)

    # Click each checkbox via JS
    res = pg.evaluate("""() => {
        const cbs = document.querySelectorAll('input[type="checkbox"]');
        const results = [];
        cbs.forEach(cb => {
            if (!cb.checked) {
                cb.click();
            }
            results.push({id: cb.id, checked: cb.checked});
        });
        return results;
    }""")
    print("Checkbox toggle results:", res)

    time.sleep(1)
    dismiss_timer(pg)

    cont = pg.locator("button:has-text('Continue')").last
    print("Continue button enabled?", cont.is_enabled())
    if cont.is_visible() and cont.is_enabled():
        print("Clicking Continue to start model testing...")
        cont.click(force=True)
        time.sleep(6)

    dismiss_timer(pg)
    pg.screenshot(path="scratch/step5_after_all_checked.png")
    print("Saved scratch/step5_after_all_checked.png")
