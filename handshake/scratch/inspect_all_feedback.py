import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_timeout(1000)
    
    # 1. Start timer if button exists
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        st.click()
        print("Clicked Start timer")
        page.wait_for_timeout(1000)
        
    # 2. Inspect feedback panel
    # Let's take screenshot
    page.screenshot(path="scratch/feedback_visible.png")
    
    # Extract feedback cards text and address status
    cards = page.evaluate("""() => {
        // Find right-side container
        const allDivs = Array.from(document.querySelectorAll('div'));
        // Find elements with checkmark or slash buttons
        const actionButtons = Array.from(document.querySelectorAll('button')).filter(b => {
            const svg = b.querySelector('svg');
            return svg && (b.getAttribute('aria-label') || '').toLowerCase().includes('resolve') || b.title;
        });
        
        // Find all feedback cards
        // In the screenshot, each card has a title like 'Image quality issue', 'Science Judge - Lumiere', 'Minor issue'
        const headers = Array.from(document.querySelectorAll('h3, h4, div[class*=\"font-\"], span[class*=\"font-\"]'))
            .filter(el => ['Image quality issue', 'Science Judge - Lumiere', 'Minor issue'].some(t => el.innerText.includes(t)));
            
        return headers.map(h => {
            const card = h.closest('div.border, div.rounded, div.p-4, div.p-3') || h.parentElement;
            return {
                title: h.innerText.trim(),
                fullText: card ? card.innerText.trim() : '',
                buttons: card ? Array.from(card.querySelectorAll('button')).map(btn => ({
                    text: btn.innerText.trim(),
                    aria: btn.getAttribute('aria-label') || '',
                    title: btn.getAttribute('title') || '',
                    svg: btn.querySelector('svg') ? btn.querySelector('svg').innerHTML.slice(0, 50) : ''
                })) : []
            };
        });
    }""")
    
    print(f"Found {len(cards)} feedback cards:")
    for i, c in enumerate(cards):
        print(f"\n--- Card {i}: {c['title']} ---")
        print(c['fullText'])
        print("Buttons:", c['buttons'])
