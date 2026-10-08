import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        tasks = await page.evaluate('''() => {
            // Find rows or cards in the task table
            const rows = Array.from(document.querySelectorAll('div, tr, li')).filter(el => {
                const text = el.innerText || '';
                return text.includes('Fix in progress') || text.includes('In progress') || text.includes('Stage');
            });
            
            // Look for task cards containing task IDs
            const taskCards = Array.from(document.querySelectorAll('*')).filter(el => {
                const t = el.innerText || '';
                return /\\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\\b/.test(t) && el.innerText.length < 500 && el.innerText.length > 50;
            });
            
            return taskCards.map(c => {
                const match = c.innerText.match(/\\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\\b/);
                const btn = c.querySelector('button');
                return {
                    taskId: match ? match[0] : null,
                    text: c.innerText.replace(/\\n+/g, ' -- '),
                    btnText: btn ? btn.innerText.trim() : null
                };
            });
        }''')
        print(f"Tasks found ({len(tasks)}):")
        for t in tasks:
            print(f"- Task: {t['taskId']} | Button: {t['btnText']}")
            print(f"  Text: {t['text'][:120]}")

if __name__ == "__main__":
    asyncio.run(main())
