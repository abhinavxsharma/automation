import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        info = await page.evaluate('''() => {
            // Find all feedback items / tabs
            const feedbackContainer = document.querySelector('[class*="feedback"], [data-testid*="feedback"]') || document.body;
            
            const comments = Array.from(document.querySelectorAll('div, li')).filter(el => {
                return (el.innerText || '').includes('Jimson') && el.innerText.length < 500 && el.innerText.length > 20;
            }).map(el => ({
                text: el.innerText.replace(/\\n+/g, ' -- '),
                buttons: Array.from(el.querySelectorAll('button, input[type="checkbox"]')).map(b => b.innerText || b.type)
            }));
            
            // Check for tabs (All, Needs attention, etc.)
            const tabs = Array.from(document.querySelectorAll('button, [role="tab"]')).filter(b => {
                const t = b.innerText.trim();
                return ['Feedback', 'All', 'Needs attention', 'QC', 'Science Judge'].includes(t);
            }).map(b => ({
                text: b.innerText.trim(),
                selected: b.getAttribute('aria-selected') || b.className.includes('active') || b.className.includes('selected')
            }));
            
            return {
                tabs,
                comments: comments.slice(0, 10)
            };
        }''')
        print("Feedback Tabs:", info.get("tabs"))
        print("\nComments found:")
        for c in info.get("comments", []):
            print(f"- {c['text'][:150]} (buttons: {c['buttons']})")

if __name__ == "__main__":
    asyncio.run(main())
