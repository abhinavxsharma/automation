import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    text = page.evaluate("() => document.body ? document.body.innerText : ''")
    print(f"Total characters in document.body.innerText: {len(text)}")
    matching = [l.strip() for l in text.split("\n") if any(k in l for k in ["Distractor", "Final", "Answer", "76", "75", "85", "Science"])]
    print("Matching lines:")
    for m in matching:
        print("  ", m)
