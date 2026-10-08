import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    page.wait_for_timeout(1000)

    # 1. Dismiss modal
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0:
        box = st_btn.first.bounding_box()
        if box:
            print("Clicking Start timer at", box)
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    page.keyboard.press("Escape")
    page.wait_for_timeout(500)

    # 2. Extract feedback panel items
    fb_data = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const feedbackStart = bodyText.indexOf('Feedback');
        const feedbackSection = feedbackStart !== -1 ? bodyText.slice(feedbackStart) : 'No Feedback section';

        // Find all cards in feedback panel
        const items = [];
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, div[class*="font-semibold"], div[class*="font-bold"]'));
        
        return {
            feedbackSection,
            allTextLength: bodyText.length
        };
    }""")

    with open("scratch/feedback_panel_text.txt", "w", encoding="utf-8") as f:
        f.write(fb_data["feedbackSection"])

    # 3. Find Image Description text
    desc_data = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.includes('Write a detailed description of your image') && e.children.length === 0);
        if (!el) return { error: 'Header not found' };
        let card = el;
        for (let i = 0; i < 6; i++) {
            if (card.parentElement) card = card.parentElement;
        }
        return {
            cardText: card.innerText
        };
    }""")

    with open("scratch/desc_card_text.txt", "w", encoding="utf-8") as f:
        f.write(desc_data.get("cardText", ""))

    # 4. Find Science Judge justification field text
    sj_data = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.includes('Pay close attention to the Science Judge') && e.children.length === 0);
        if (!el) return { error: 'Science Judge section not found' };
        let card = el;
        for (let i = 0; i < 6; i++) {
            if (card.parentElement) card = card.parentElement;
        }
        return {
            cardText: card.innerText
        };
    }""")

    with open("scratch/sj_card_text.txt", "w", encoding="utf-8") as f:
        f.write(sj_data.get("cardText", ""))

    page.screenshot(path="scratch/current_overview.png")
    print("Done! Check files in scratch/")
