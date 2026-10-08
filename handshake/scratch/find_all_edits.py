import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.append(str(Path(__file__).parent))
from chrome_helper import get_task_page


def main():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        page.wait_for_selector("text=Computer Systems", timeout=15000)
        
        edit_btns = page.locator("button[aria-label*='Edit']").all()
        print(f"Total edit buttons found: {len(edit_btns)}")

        for i, btn in enumerate(edit_btns):
            aria_label = btn.get_attribute("aria-label")
            # find enclosing text
            parent_text = btn.evaluate("""
                el => {
                    let cur = el.parentElement;
                    for (let step = 0; step < 6; step++) {
                        if (!cur || cur === document.body) break;
                        if (cur.innerText && cur.innerText.trim().length > 10) return cur.innerText.substring(0, 150);
                        cur = cur.parentElement;
                    }
                    return 'N/A';
                }
            """)
            print(f"Btn {i}: aria='{aria_label}' -> {repr(parent_text)}")


if __name__ == "__main__":
    main()
