import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.append(str(Path(__file__).parent))
from chrome_helper import get_task_page


def dismiss_timer(page):
    btn = page.locator("button:has-text('Start timer')")
    if btn.count() > 0 and btn.first.is_visible():
        box = btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)


def main():
    with sync_playwright() as p:
        browser, page = get_task_page(p)
        print("Page URL:", page.url)
        page.wait_for_timeout(2000)
        dismiss_timer(page)
        page.screenshot(path="handshake/scratch/resume_check.png")
        print("Screenshot saved to handshake/scratch/resume_check.png")

        # Check Step 7 editor or general text
        body_text = page.locator("body").inner_text()
        print("Body text length:", len(body_text))
        for line in body_text.split("\n"):
            line_s = line.strip()
            if any(k in line_s for k in ["Step 7", "Step 8", "15 / 15", "needs attention", "Changes saved", "Submit Task", "Upload files", "Draft"]):
                print("Line:", line_s)


if __name__ == "__main__":
    main()
