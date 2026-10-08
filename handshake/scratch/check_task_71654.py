import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        print("Navigating to task 71654a38...")
        await page.goto("https://ai.joinhandshake.com/annotations/fellow/task/71654a38-62f6-4977-9953-bb5f5e3eb7cc/run")
        await asyncio.sleep(4.0)
        
        info = await page.evaluate('''() => {
            const banner = document.querySelector('[class*="banner"], [role="alert"], [class*="alert"]');
            const h = Array.from(document.querySelectorAll('h1, h2, h3, h4')).map(e => e.innerText.trim()).filter(Boolean);
            const feedbackItems = Array.from(document.querySelectorAll('div, li, p')).filter(el => {
                const t = el.innerText || '';
                return t.includes('Model Response 1 final answer') || t.includes('Both model responses must genuinely fail') || t.includes('Your task was sent back');
            }).map(el => el.innerText);
            
            const promptEl = document.querySelector('[data-block-id="9e254568-dd1a-476f-9eb5-d49807d95930"]') || document.querySelector('[data-testid*="prompt"]');
            
            return {
                url: window.location.href,
                title: document.title,
                bannerText: banner ? banner.innerText : null,
                feedbackItems: feedbackItems.slice(0, 5),
                promptSnippet: promptEl ? promptEl.innerText.slice(0, 200) : null
            };
        }''')
        print("Task 716 URL:", info['url'])
        print("Task 716 Title:", info['title'])
        print("Banner:", info['bannerText'])
        print("Feedback items found:")
        for item in info['feedbackItems']:
            print("---")
            print(item[:300])

if __name__ == "__main__":
    asyncio.run(main())
