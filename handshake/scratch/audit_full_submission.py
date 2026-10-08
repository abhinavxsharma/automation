import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_timeout(1000)

    # 1. Click "All" tab in Feedback panel to check all automated checkers
    all_tab = page.locator("button:has-text('All'), div[role='tab']:has-text('All')").first
    if all_tab.count() > 0:
        all_tab.click()
        page.wait_for_timeout(1000)

    page.screenshot(path="scratch/feedback_all_tab.png")

    feedback_all_text = page.evaluate("""() => {
        const fbStart = document.body.innerText.indexOf('Feedback');
        return fbStart !== -1 ? document.body.innerText.slice(fbStart) : 'No feedback found';
    }""")

    # 2. Extract full page text and inspect key sections
    full_text = page.evaluate("() => document.body.innerText")

    with open("scratch/audit_full_page_text.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    # 3. Key section audits
    audit = page.evaluate("""() => {
        const text = document.body.innerText;
        return {
            isReadOnly: text.includes('This is in read only mode.'),
            hasPrompt: text.includes('critical path duration (maximum latency from S to T)'),
            hasAnswer76: text.includes('Final Answer:') && text.includes('76'),
            descHas400Words: text.includes('Multiple edges cross each other in the two-dimensional planar layout') && text.includes('eight distinctly labeled circular nodes'),
            descHasDuplicate: (text.match(/The figure displays a directed acyclic graph/g) || []).length > 2,
            sjHasJustification: text.includes('The Science Judge flag (AMBIGUOUS_PROMPT) is a clear automated false positive'),
            feedbackSnippet: text.slice(text.indexOf('Feedback'), text.indexOf('Feedback') + 1500)
        };
    }""")

    with open("scratch/final_audit_summary.json", "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2)

    print("Audit summary:", json.dumps(audit, indent=2))
