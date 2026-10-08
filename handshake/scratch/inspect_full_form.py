import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # Dismiss timer modal if present
    timer_btn = page.locator("button:has-text('Start timer')")
    if timer_btn.count() > 0:
        box = timer_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(500)

    # Check if feedback sidebar is open
    is_open = page.evaluate("""() => {
        return !!document.querySelector('aside') || document.body.innerText.includes('Feedback');
    }""")
    print("Feedback open?", is_open)

    # Extract all text and buttons
    info = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            className: b.className
        })).filter(b => b.text || b.aria);

        return {
            bodyTextLength: bodyText.length,
            feedbackFound: bodyText.includes('Feedback'),
            buttons: buttons
        };
    }""")

    print(f"Body text length: {info['bodyTextLength']}, Feedback found: {info['feedbackFound']}")
    print(f"Buttons found: {len(info['buttons'])}")

    # Save complete body text to inspect every section
    full_text = page.evaluate("() => document.body.innerText")
    with open("scratch/full_page_body_text.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    page.screenshot(path="scratch/inspect_full.png")
    print("Saved body text to scratch/full_page_body_text.txt and screenshot to scratch/inspect_full.png")
