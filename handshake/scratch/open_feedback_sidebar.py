import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # 1. Dismiss timer modal if present
    timer_btn = page.locator("button:has-text('Start timer')")
    if timer_btn.count() > 0:
        box = timer_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(500)

    # 2. Inspect all buttons in header
    header_info = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('header button, div[class*="sticky"] button, div[class*="border-b"] button'));
        return btns.map((b, i) => ({
            index: i,
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            title: b.getAttribute('title') || '',
            innerHTML: b.innerHTML.slice(0, 100),
            rect: b.getBoundingClientRect()
        }));
    }""")
    print("Header buttons:", json.dumps(header_info, indent=2))

    # Click the toggle button (the one with icon or feedback)
    # Usually it's the 4th button or has svg
    for b in header_info:
        if b['text'] not in ['Save', 'Exit'] and b['rect']['width'] > 0:
            print(f"Clicking header button: {b}")
            page.mouse.click(b['rect']['x'] + b['rect']['width'] / 2, b['rect']['y'] + b['rect']['height'] / 2)
            page.wait_for_timeout(1000)
            break

    page.screenshot(path="scratch/after_toggle_click.png")
    
    # Check if feedback is visible now
    fb_text = page.evaluate("""() => {
        const body = document.body.innerText;
        return {
            hasFeedback: body.includes('Feedback'),
            snippet: body.includes('Feedback') ? body.slice(body.indexOf('Feedback'), body.indexOf('Feedback') + 1500) : ''
        };
    }""")
    print("Feedback visible?", fb_text['hasFeedback'])
    if fb_text['hasFeedback']:
        print("Snippet:", fb_text['snippet'])
