import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        print("Navigating to task 1520c7f4...")
        await page.goto("https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run")
        await asyncio.sleep(4.0)
        
        info = await page.evaluate('''() => {
            const banner = document.querySelector('[class*="banner"], [role="alert"], [class*="alert"]');
            const feedbackItems = Array.from(document.querySelectorAll('div, li, p')).filter(el => {
                const t = el.innerText || '';
                return t.includes('Model Response 1 final answer') || t.includes('Both model responses must genuinely fail') || t.includes('Your task was sent back');
            }).map(el => el.innerText);
            
            return {
                url: window.location.href,
                title: document.title,
                banner: banner ? banner.innerText : null,
                feedbackItems: feedbackItems.slice(0, 5),
                bodyText: document.body.innerText.slice(0, 1000).replace(/\\n+/g, ' -- ')
            };
        }''')
        print("Task 1520 URL:", info['url'])
        print("Task 1520 Title:", info['title'])
        print("Banner:", info['banner'])
        print("Feedback items found:")
        for item in info['feedbackItems']:
            print("---")
            print(item[:300])
        print("\nBody text:\n", info['bodyText'][:500])

if __name__ == "__main__":
    asyncio.run(main())
